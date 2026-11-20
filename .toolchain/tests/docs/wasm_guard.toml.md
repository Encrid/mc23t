# .toolchain/tests/cases/wasm_guard.toml

The group `wasm_guard` checks `.toolchain/tools/wasm_guard.py`.
Each case writes the bytes of a file into `{case}/m.wasm` with `files`, and runs `wasm_guard.py` on that file.
Each file starts with the wasm magic and the version 1, except in the first case.
The case `a wasm module with the accessors` of the group `presets` runs the guard in a build.

| Case | Claim | False variant |
| --- | --- | --- |
| a file that is not a wasm module | The file holds `text`. `wasm_guard.py` writes `is refused: it is not a wasm module`, and ends with 1. | The file holds the magic and the version, and no section. |
| a module that imports a memory | The import section holds the memory `m.s`. `wasm_guard.py` writes `is refused: it imports the memory 'm.s'; a module reaches shared data only through the accessors`. | The import is a function. |
| a module that imports a global | The import section holds the global `m.g`. `wasm_guard.py` writes `is refused: it imports the global 'm.g'; a module imports no global`. | The import is a function. |
| a module that imports a tag | The import section holds the tag `m.t`. `wasm_guard.py` writes `is refused: it imports the tag 'm.t'; a module imports no tag`. | The import is a function. |
| a table with a maximum is stepped over | The import section holds the table `m.t` with a minimum and a maximum, then the global `m.g`. `wasm_guard.py` writes the refusal of the global. | The second import is a function. |
| a module that ends inside the import section | The file ends after the identifier of the import section. `wasm_guard.py` writes `is refused: it ends inside a section`. | The import section has its size and 0 imports. |
| a module that ends inside a different section | The type section states 5 bytes, and the file holds 1. `wasm_guard.py` writes `is refused: it ends inside a section`. | The type section states 1 byte. |
