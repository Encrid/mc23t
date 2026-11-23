# .toolchain/tests/cases/rewrite.toml

The group `rewrite` checks how `parsed` of `.toolchain/tools/rewrite.py` reads a syntax tree: `.toolchain/docs/rewrite.py.md`, *The syntax tree*.
Each case writes a small tree into `{case}/tree.json` with `files`. The root of the project is `/r`.
Each case sets the size of a part to 100 characters. Thus a node continues into the next part, and `parsed` also drops the text that it read.
The cases of the groups `branches`, `leaks` and `fail` run `parsed` on the trees of real files, in parts of 16 MiB.

| Case | Claim | False variant |
| --- | --- | --- |
| a syntax tree read in small parts keeps the nodes that a run reads | The tree holds a `typedef` with no location, `malloc` of a header of the system with 1 parameter, a `struct` of that header, the function `go` of `/r/src/a.c` with its body, and the variable `kept` with no file in its location. `parsed` keeps `malloc` with its parameter, `go` whole, and `kept` with the file `/r/src/a.c` of the location before it. It drops the `struct`. | `go` is in the header `/usr/include/go.h`. Thus `kept` is in that header too. |
| a syntax tree that ends too soon is not JSON | The tree has no `]` at the end of its top. `parsed` gives `ValueError`, and the case writes `the tree ends too soon`. | The tree ends with `]}`. |
