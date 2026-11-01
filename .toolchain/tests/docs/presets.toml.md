# .toolchain/tests/cases/presets.toml

The group `presets` checks the presets of `.toolchain/presets`.
Its first case copies the files of a preset into a project in `{case}/proj`, then runs `fetch.py` and `build.py` on that project.
Thus the case fetches the 3 sources of the preset on each target, and checks their urls and their sha256.
Its second case copies only the kind of the preset, and builds a module for `x86_64-windows-gnu` on each target, with nothing to fetch.
It reads the imports of the module with `tools/inspect.py` of `.toolchain/tests/data/build/runtime`.

`.toolchain/tests/data/presets` holds the other files of the project:

| File | Content |
| --- | --- |
| `project.toml` | The artifact `probe` of the kind `native_module`. Its manifest states the identity `test:probe@1.0.0`, `abi=3`, `config=none`, `pinned=false` and `reloadable=false`. |
| `probe.c` | A native module of the ABI 3 of Bridge. It exports `init`, `reload` and `shutdown`, and adds the systems `tick` and `tock`. `tock` gives the slot of `tick` in `before`, as the macros of BB-Native need. It puts the manifest into its section. |
| `unmarked/probe.c` | The same module, without the manifest. |
| `runtime/project.toml` | The artifact `probe` of the kind `native_module`. It gives the variables `bridge` and `bb_native`, and the section of `x86_64-windows-gnu`, which the preset takes from its sources. |
| `runtime/probe.c` | A module with its manifest and one function, which needs no header of Bridge. |
| `runtime/bare_kinds.toml` | The kind `native_module` as it was before it linked `{runtime}`. |

| Case | Claim | False variant |
| --- | --- | --- |
| a native module with its manifest | `fetch` and `build` end with 0, and `build` writes the path of `probe{library}`. | The module without the manifest. Thus the step `contains` stops the build. |
| a native module of x86_64-windows-gnu takes its moves and its fills from Windows | `inspect.py imports` writes `KERNEL32.dll: RtlMoveMemory` and `KERNEL32.dll: RtlFillMemory` for `probe.dll`. | `runtime/bare_kinds.toml` in place of the kind of the preset: the module imports neither. |
