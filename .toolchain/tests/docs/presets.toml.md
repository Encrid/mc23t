# .toolchain/tests/cases/presets.toml

The group `presets` checks the presets of `.toolchain/presets`.
Its first case copies the files of a preset into a project in `{case}/proj`, then runs `fetch.py` and `build.py` on that project.
Thus the case fetches the 3 sources of the preset on each target, and checks their urls and their sha256.
Its second case copies only the kind of the preset, and builds a module for `x86_64-windows-gnu` on each target, with nothing to fetch.
It reads the imports of the module with `tools/inspect.py` of `.toolchain/tests/data/build/runtime`.

Its third case copies the files of the preset `wasm_module`, with the sources of `native_module`, and builds a wasm module from C. Its fourth case builds a module of wasm text. Its fifth case reads the manifest in the built module. Its sixth case builds a wasm library, and a wasm module that links it. Its seventh case builds the same project with a different `float`.

`.toolchain/tests/data/presets` holds the other files of the project:

| File | Content |
| --- | --- |
| `project.toml` | The artifact `probe` of the kind `native_module`. Its manifest states the identity `test:probe@1.0.0`, `abi=1`, `config=none`, `pinned=false` and `reloadable=false`. |
| `probe.c` | A native module of the ABI 1 of Bridge. It exports `init`, `reload` and `shutdown`, and adds the systems `tick` and `tock`. `tock` gives the slot of `tick` in `before`, as the macros of BB-Native need. It puts the manifest into its section. |
| `unmarked/probe.c` | The same module, without the manifest. |
| `runtime/project.toml` | The artifact `probe` of the kind `native_module`. It gives the variables `bridge` and `bb_native`, and the section of `x86_64-windows-gnu`, which the preset takes from its sources. |
| `runtime/probe.c` | A module with its manifest and one function, which needs no header of Bridge. |
| `runtime/bare_kinds.toml` | The kind `native_module` as it was before it linked `{runtime}`. |
| `wasm/project.toml` | The artifact `probe` of the kind `wasm_module`. It links `{bb_wasm}/acc.wasm`, includes the headers of Bridge and of BB-Wasm, and states the manifest `test:probe@1.0.0`. |
| `wasm/unmarked/project.toml` | The same artifact, with no manifest. |
| `wasm/probe.c` | A wasm module with 1 component and the system `step`, which reads and writes it through the accessors. |
| `wasm/imports/project.toml` | The same artifact, linked with `-Wl,--import-memory`, so the module imports `env.memory`. |
| `wasm/text/project.toml` | The artifact `probe` of the kind `wasm_text`. |
| `wasm/text/probe.wat` | A module of wasm text that exports `init`. |
| `wasm/text/broken/probe.wat` | The same text, with an `i32.const` that has no number. |
| `wasm/library/project.toml` | The artifact `sums` of the kind `wasm_library`, with `-ffp-contract=off`, and the artifact `probe` of the kind `wasm_module`, which names `{out}/sums.a` in `archives`. |
| `wasm/library/unlinked/project.toml` | The same artifacts, and `probe` names no archive. |
| `wasm/library/sums.c` and `wasm/library/sums.h` | The function `sums_get_next`, which gives its value plus 1. |
| `wasm/library/probe.c` | The module of `wasm/probe.c`, whose system `step` calls `sums_get_next`. |

| Case | Claim | False variant |
| --- | --- | --- |
| a native module with its manifest | `fetch` and `build` end with 0, and `build` writes the path of `probe{library}`. | The module without the manifest. Thus the step `contains` stops the build. |
| a native module of x86_64-windows-gnu takes its moves and its fills from Windows | `inspect.py imports` writes `KERNEL32.dll: RtlMoveMemory` and `KERNEL32.dll: RtlFillMemory` for `probe.dll`. | `runtime/bare_kinds.toml` in place of the kind of the preset: the module imports neither. |
| a wasm module with the accessors | `fetch` and `build` end with 0, and `build` writes the path of `probe.wasm`. | The module imports a memory. Thus `wasm_guard.py` stops the build. |
| a module of wasm text | `fetch` and `build` end with 0, and `build` writes the path of `probe.wasm`. | The text is not valid. Thus `wasm-as` stops the build. |
| a wasm module with its manifest | The built module holds the section `bridge:manifest` and the identity `test:probe@1.0.0`. | The artifact states no manifest. |
| a wasm library that a wasm module links and calls | `fetch` and `build` end with 0, and `build` writes the paths of `sums.a` and of `probe.wasm`. | `probe` names no archive. Thus `wasm-ld` finds no `sums_get_next`, and stops the build. |
| a wasm library compiles with the rules of floating point | With `--set float=-fno-such-flag`, the compile of `sums.c` for `-target wasm32-freestanding` stops: `unknown clang option: "-fno-such-flag"`. Thus `wasm_compile` holds `{float}`. | `float` is `-ffp-contract=off`, a flag that clang knows. |
