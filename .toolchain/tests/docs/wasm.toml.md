# .toolchain/tests/cases/wasm.toml

The group `wasm` checks the probes of `test --branches` and the counts of `test --leaks` in a wasm module.
Its one case is a table. It copies the files of the preset `wasm_module` and the files of `.toolchain/tests/data/wasm` into a project in `{case}/proj`.
Then it runs `tools/drive.py` of `.toolchain/tests/data/wasm`, which fetches the sources of the project 1 time, and answers each row.

`drive.py` reads 1 line for each row: a run, and the words of `-k`. `build` runs `build.py`, `branches` runs `test.py --branches`, and `leaks` runs `test.py --leaks`.
It writes the last line of the run, then the exports and the area of the module with `tools/area.py`.
`area.py` reads the module as a host reads it: the global `c23b_outcomes`, the area, and each chunk: `.toolchain/docs/outcomes.h.md`, *A host of wasm modules*.

| File | Content |
| --- | --- |
| `project.toml` | The artifact `probe` of the kind `wasm_module`, from `src/heap.c` and `src/probe.c`, and the test program `stand_in`. |
| `src/heap.c` | `malloc` and `free` of the module. `malloc` gives bytes of a static array. |
| `src/probe.c` | The export `pick`, which takes a block with `malloc`, tests it, and frees it. Thus its file gets the layer of `fail` and the count of `memory`. |
| `tests/stand_in.c` | A stand-in of a host. It gives bytes 1 to `c23_outcomes_keep`, for the first byte and the number of bytes of its arguments, and writes `kept` or `refused`. |
| `tests/cases/stand_in.toml` | The case `a host keeps the outcomes of the module` gives the 12 bytes of the 2 files. The case `a host that writes past the end of the file keeps nothing` gives 13 bytes. |

| Row | Claim | False input |
| --- | --- | --- |
| a wasm module with no probes exports nothing | The normal build gives a module whose only exports are `memory` and `pick`. | `branches` |
| a probed wasm module exports the area of its outcomes | After `--branches`, the module exports `c23b_outcomes`. Its area holds 2 chunks of 6 bytes, at the bytes 0 and 6 of the file of the hits. | `build` |
| the outcomes that a host keeps reach hits.bin | With the stand-in, `--branches` writes `branches: 9 outcomes, 9 reached`. | `branches past`: only the stand-in that writes past the end runs, so no outcome is reached. |
| a probed wasm module exports the counts of its leaks | After `--leaks`, the area holds the chunk of counts of `src/probe.c`, with 2 counts. | `branches` |

## Limits

No case runs a wasm module, because no host in this project reads the area. The stand-in gives the bytes that a host reads.
