# .toolchain/tests/cases/branches.toml

The group `branches` checks `.toolchain/tools/branches.py`, through `test --branches` of `.toolchain/tools/test.py`.
Each case runs `test.py` on a project of `.toolchain/tests/data/branches`, with its output in `{case}/out`.

| Project | Content |
| --- | --- |
| `missed` | The program `branchy` and its header `branchy.h`. One case runs it with `1`. Thus one function, two labels and six outcomes of conditions are not reached. One test with `\|\|` is in an argument of the macro `CHECKED`. |
| `reached` | The same program, with no function that no case calls and no macro. Four cases reach each outcome. |
| `empty` | A project with no source and no case. |
| `excused` | The program `defend`, whose guard no case reaches, and an exemption of `project.toml` that excuses the guard. |
| `badexempt` | The same program, with an exemption that states no reason and an exemption that matches no outcome. |
| `systemed` | The same program, with the exemption of `excused` for the system `elsewhere`. |
| `loaded` | The library `chooser`, with one condition, and the test program `loader` that opens it, calls it and closes it. The case `both` calls it with 1 and with 0. The case `one` calls it with 1. |
| `ended` | The program `ender`. With the argument `exit` it ends with `_Exit(1)`, with a different argument it calls `abort`, and with no argument it ends with 0. Its three cases run the three paths. Only the paths of `_Exit` and of `abort` make the condition `count > 1` true. |
| `expanded` | The program `macros`. Its conditions touch calls of `TWICE`, `SAME` and `PICK`. The test in `PICK`, the 2 tests of `BOTH` and the test of `IFPOS` hold only a part of a call. Its cases `none`, `two` and `three` reach each outcome. |
| `embedded` | The program `show`, which embeds `word.txt` with `#embed` and no byte after it. `word.txt` is an input, which the run builds after the dump. With an argument the program writes the argument, else it writes `one`. Its cases `word` and `argument` reach each outcome. |
| `shared` | The parts `core` and `app`. The program `core` builds `core.c` and `core_main.c`, and its 2 cases reach each outcome of `core`. The program `app` builds `app.c` and `core.c`, and includes `core.h`. Its 3 cases reach each outcome of `app.c`, but not each outcome of `core.c` and `core.h`. The case `app without memory` makes the first `malloc` fail. |

| Case | Claim | False variant |
| --- | --- | --- |
| branches that no case reaches | `test` writes a line for a function, a label, a condition never false, a condition never true, a condition in a macro and a condition of the header. Then it writes `branches: 17 outcomes, 9 reached`, and stops. | The project `reached`. |
| each branch reached | `test` writes `branches: 16 outcomes, 16 reached`, and ends with 0. | The project `missed`. |
| branches of a project with no source | `test` writes `branches: 0 outcomes, 0 reached`, and ends with 0. | The project `reached`. |
| branches with a false variant | `test --branches --break` stops: `--branches runs each case one time`. | No `--break`. |
| an exemption excuses an unreached branch | `test` writes `branches: 4 outcomes, 3 reached, 1 exempt`, and ends with 0. | The project `badexempt`. |
| an outcome stays when the program ends with _Exit or abort | `test` on `ended` writes `branches: 7 outcomes, 7 reached`, and ends with 0. | `-k plain`, thus no case ends with `_Exit` or `abort`. |
| a closed library keeps its outcomes | `test` writes `branches: 3 outcomes, 3 reached`, and ends with 0. On macOS this needs the constructor that keeps the library mapped. | `-k one`, thus the condition is never false. |
| a probe holds each call of a macro in full | `test` on `expanded` writes 3 conditions as not measured, at `src/macros.c:28:14`, `30:9` and `32:5`. It writes `branches: 17 outcomes, 17 reached`, and stops. | `-k none`, thus 9 outcomes are not reached. |
| an exemption for a different system does not apply | `test` on `systemed` writes `src/defend.c:10:9: no case makes this condition true`, and stops. No line names the exemption. | The project `excused`. |
| an exemption with no reason or no target is a fault | `test` writes the unreached branch, `this exemption states no reason` and `this exemption excuses no unreached outcome`, and stops. | The project `excused`. |
| a program that embeds an input is measured | `test` on `embedded` writes `branches: 3 outcomes, 3 reached`, and ends with 0. The dump finds a stand-in of `word.txt`, so the array is not empty. | `-k word`, thus the condition is never true. |
| a run of a part measures only the files of its part | `test --part app` on `shared` writes `branches: measured parts app` and `branches: 3 outcomes, 3 reached`, and ends with 0. No line names `src/core`. | No `--part`, thus no line names the measured parts. |
| a run of a part with no use measures its own files | `test --part core` on `shared` writes `branches: measured parts core` and `branches: 9 outcomes, 9 reached`. | `--part app`. |
| a full run measures the files of each part | `test` on `shared` writes `branches: 12 outcomes, 12 reached`, and names no measured parts. | `--part app`, thus 3 outcomes. |
| a run of a part keeps the layer of fail in the files of other parts | `test --part app` on `shared` writes `app without memory: as written`. `core.c` has no probes, but it keeps the layer that makes `malloc` fail. | `-k "app one"`, thus that case does not run. |
| a run of a group measures only the code that the group tests | `test --branches --group app/app` on `shared` writes `branches: measured the code of the groups app/app` and `branches: 3 outcomes, 3 reached`, and names no file of `src/core`. | No `--group`. |
| the cases of a group reach each branch of the code that the group tests | With `-k "app one"`, the group `app/app` does not reach one outcome of `app.c`, and the run fails: `outcomes not reached: 1`. | No `-k`. |
| a file is measured only when each group that tests it runs | The project `grouped` has one source, and its groups `one` and `two` state no `code`. `test --branches --group one` measures no file: `branches: 0 outcomes, 0 reached`. | The 2 groups: 3 outcomes. |
| the groups that test a file reach its branches together | `test --branches --group one --group two` on `grouped` writes `branches: 3 outcomes, 3 reached`. | `-k one`, thus the case of `two` does not run, and one outcome is not reached. |
