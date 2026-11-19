# .toolchain/tests/cases/wasm.toml

The group `wasm` checks the probes of `test --branches` and the counts of `test --leaks` in a wasm module.
Its one case is a table. It copies the files of the preset `wasm_module` and the files of `.toolchain/tests/data/wasm` into a project in `{case}/proj`.
Then it runs `tools/drive.py` of `.toolchain/tests/data/wasm`, which fetches the sources of the project 1 time, and answers each row.

`drive.py` reads 1 line for each row: a run, and the words of `-k`. `build` runs `build.py`, `branches` runs `test.py --branches`, and `leaks` runs `test.py --leaks`.
It writes the line of the group `stand_in` and the last line of the run, then the exports and the area of the module with `tools/area.py`.

The run `fail` builds the module of `test --branches` 1 time, and keeps it. Then `tools/host.py` runs it, as a host of wasm modules does.
The words after `fail` are the plan: each word `<name>=<value>` goes into the text of `C23_FAIL`, after a space, and `part:<name>` gives the text of `C23_FAIL_PART`.
`host.py` loads `wasmtime` of the source `bb_wasm`, and starts an instance with no import. It writes the plan into the area, and calls `pick(1)`, `pick(2)` and `pick(3)`.
Then it writes `pick:` and the 3 results, and `plan:` and the text of `C23_FAIL` that the module holds after the calls.
`area.py` reads the module as a host reads it: the global `c23b_outcomes`, the area, and each chunk: `.toolchain/docs/outcomes.h.md`, *A host of wasm modules*.

| File | Content |
| --- | --- |
| `project.toml` | The artifact `probe` of the kind `wasm_module`, from `src/heap.c` and `src/probe.c`, and the test program `stand_in`. |
| `src/heap.c` | `malloc` and `free` of the module. `malloc` gives bytes of a static array. |
| `src/probe.c` | The export `pick`, which takes a block with `malloc`, tests it, and frees it. Thus its file gets the layer of `fail` and the count of `memory`. |
| `tests/stand_in.c` | A stand-in of a host. It gives bytes 1 to `c23_outcomes_keep`, for the first byte and the number of bytes of its arguments, and writes `kept` or `refused`. |
| `tools/host.py` | A host of wasm modules, in Python, with the C API of `wasmtime`: `.toolchain/docs/outcomes.h.md`, *The steps of the host*, steps 1 and 2. |
| `tests/cases/stand_in.toml` | The case `a host keeps the outcomes of the module` gives the 12 bytes of the 2 files. The case `a host that writes past the end of the file keeps nothing` gives 13 bytes. |

| Row | Claim | False input |
| --- | --- | --- |
| a wasm module with no probes exports nothing | The normal build gives a module whose only exports are `memory` and `pick`. | `branches` |
| a probed wasm module exports the area of its outcomes | After `--branches`, the module exports `c23b_outcomes`. Its area has the version 1 and the room 256, and holds 2 chunks of 6 bytes, at the bytes 0 and 6 of the file of the hits. | `build` |
| the outcomes that a host keeps reach hits.bin | With the stand-in, `--branches` writes `branches: 9 outcomes, 9 reached`. | `branches past`: only the stand-in that writes past the end runs, so no outcome is reached. |
| a probed wasm module exports the counts of its leaks | After `--leaks -k past`, the area holds the chunk of counts of `src/probe.c`, with 2 counts, and the case of the stand-in passes. With no `-k`, the case `a host keeps the outcomes of the module` writes `refused`, because `--leaks` sets no `C23_BRANCHES`. | `branches past` |
| a module with no plan fails no call | With an empty plan, each call of `malloc` gives a block: `pick: 1 1 1`. | `fail malloc=1` |
| the plan of the host makes the call of its number fail | With `malloc=2`, the second call of `malloc` fails: `pick: 1 -1 1`. | `fail malloc=3` |
| a call that fails writes told=1 into the plan | With `malloc=2 told=0`, the failed call writes `1` in place of the `0`: `plan: malloc=2 told=1`. | `fail malloc=4 told=0`: no fourth call, so no call fails. |
| a plan for a different part fails no call | With `part:other`, the text of the parts of the file does not hold `other`: `pick: 1 1 1`. | `fail malloc=2 part:`, an empty part. |

## Limits

`host.py` does only the steps 1 and 2 of the host. The stand-in gives the bytes that a host reads at the end of an instance.
The run `fail` needs `wasmtime` in the release of `bb_wasm` for the target of the machine.
