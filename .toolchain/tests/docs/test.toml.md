# .toolchain/tests/cases/test.toml

The group `test` checks `.toolchain/tools/test.py`.
The first thirteen cases use the keys of a case. Their commands are short Python programs, thus they need no build.
The other cases run `test.py` on a project in `{case}`. Their `folders` copy the files of `.toolchain/tests/data/test` into it.

| File | Content |
| --- | --- |
| `.toolchain/project.toml` | A project with no artifact, and a timeout of 60 seconds. |
| `note.txt` | The line `written at the prompt`. |
| `passes.toml` | The case `passes`, which passes. |
| `fails.toml` | The case `fails`, which ends with the status 1. |
| `not_text.toml` | The case `bytes`, which ends with the status 1. Its command writes `a`, the byte 255, which is not UTF-8, and `b`. |
| `table.toml` | The table `greet` with 3 rows, which claims the status 0. Its command answers each name with `hello, <name>`, and an empty line with `no name`. |
| `table_still.toml` | The same table. The false input of its first row is the input of the row. |
| `table_ends.toml` | The same table. Its command ends at the name `Bob`, which the second row gives. |
| `table_many.toml` | The same table. Its command writes 2 answers for each row. |
| `long_table.py` | A program that writes the table `long` into the project, and runs `test` on it. The table has 60 rows. Each input has 2000 characters, and each answer is 10 times its input. Each row claims the text that the program gets. |
| `table_paced.toml` and `table_stalls.toml` | The table `paced`: 4 rows, and each row answers after 0.7 seconds. In the table `stalls`, the third row answers after 3 seconds. |
| `table_state.toml` | A table of 2 rows. Its command writes the number of each line before the name. |
| `table_exit.toml` | The same table as `table.toml`. Its command ends with the status 1. |
| `table_none.toml` | A table with `rows = []`. |
| `table_false.toml` | A table that also states `false`. |
| `table_short.toml` | A table whose first row has no `false`. |
| `table_status.toml` | A table whose first row claims `status`. |
| `table_whole.toml` | The table `words` with 2 rows. Its command answers a line with each of its words on a line. Each row claims `output`, with a file of `said`. |
| `table_whole_differs.toml` | The same table with 3 rows whose claim `output` is false: a file with 1 line less than the answer, a file that is not there, and an empty file. |
| `table_mute.toml` | A table whose first row has `claims = {}`. |
| `table_silent.toml` | The table of `table.toml` with no `claims` for its run. |
| `tabled/project.toml` | The project of `project.toml`, with `tables = true` in `[test]`. |
| `own_stated.toml` | The case `stated`, which passes and states `process = "status"`. The case `fed`, which passes with a `stdin` and states `process = "script"`. |
| `own_word.toml` | The case `worded`, which states `process = "speed"`. |
| `own_script.toml` | The case `silent`, which states `process = "script"` with no `script` and no `stdin`. |
| `table_own.toml` | The table of `table.toml`, which also states `process`. |
| `swept_by_hand.toml` | 3 cases with one command. Each one states `process`, and makes one call of `malloc` fail: the first, the second, the third. |
| `alone.toml` | The case `alone`, which has no false variant. |
| `silent.toml` | The case `silent`, which claims nothing. |
| `colour.toml` | The case `colour`, which has the key `colour`. |
| `signals.py` | A program that writes `ready`, reads a line, and writes `done`. It writes `paused` before `done` if 1 second went by after `ready`. It writes each line with no buffer, so a signal that comes during a write cannot make a write inside a write. |
| `signals.py`, the signals | For each signal, `signals.py` writes `got <signal>`. After a hang-up it ends with 0. If it cannot write `done`, it ends with 3. |
| `unknown_signal.toml`, `closed_input.toml`, `zero_pause.toml` and `ignored_termination.toml` | Each has one case with a value that a script or `ignore` does not allow. |
| `interrupt_termination.toml`, `after_hang_up.toml` and `wait_after_close.toml` | Each has one case with a script that cannot run the same way on each system. |
| `late.toml` and `late/project.toml` | The case `late`, which waits 9 seconds, and a timeout of 2 seconds. |
| `said.toml` and `ruled/project.toml` | The case `said`, which writes `ended after`, and a rule that refuses this text, but not in the group `free/said`. |
| `still.toml` | The case `still`, whose false variant also passes. |
| `later/project.toml` | An artifact that links `linked.txt`, which is not there. Its kind has `unlinked` steps. |
| `nowhere/project.toml` | The project of `.toolchain/project.toml`, and the target `nowhere`, whose `runs_on` is empty. |
| `port/project.toml`, `unported.toml` and `ported.toml` | A project whose variable `address` holds `{port}`. The case `unported` names `{address}` only, and the case `ported` names `{port}` too. |
| `patterned.toml` | The case `patterned`, whose `folders` copy each file of the pattern `data/*.txt` into `{case}/got`. |
| `met.py` | A program that writes its mark into a folder, and looks for the mark of another case for some seconds. With `meet`, it ends with 0 if it sees the mark. With `apart`, it ends with 0 if it does not see the mark, and then removes its own mark. |
| `met.toml` | The cases `a meets b` and `b meets a`, which wait 5 seconds for each other with `met.py`. |
| `order_1.toml` and `order_2.toml` | The case `slow`, which waits 2 seconds, and the case `quick`. |
| `linked.toml` and `copied.toml` | The case `linked`, which places `prog.txt` into `{case}/got` and writes if the placed file is the same file as its source. In `linked.toml` the source is `{build}/prog.txt`, and in `copied.toml` it is `prog.txt` of the project. |
| `overwritten.toml` and `overwrote.toml` | The case `overwritten`. In `overwritten.toml`, it places `{build}/prog.txt` into `{case}/got`, and its `files` write `changed` into the placed file. In `overwrote.toml`, its `files` write `changed` into `{build}/prog.txt`. |
| `uses/project.toml` | The project of `.toolchain/project.toml`, with the use `gpu` for `src/gpu/**` and the use `display` for `src/screen/**`. `uses/one` has only `gpu`, `uses/none` gives `gpu` no pattern, `uses/nofile` gives it `src/none/**`, and `uses/nouse` has no use. |
| `uses/drawn.toml`, `uses/both.toml` and `uses/plain.toml` | The cases `drawn`, `both` and `plain`, which pass. Their groups test `src/gpu`, `src/gpu` and `src/screen`, and `src/other`. |
| `uses/probe.toml` | The case `probe`, which writes `taken` if another process holds the lock of `gpu`, and `free` if not. |
| `uses/apart_one.toml` and `uses/apart_two.toml` | The cases `one stays apart from two` and `two stays apart from one`, which look for each other for 2 seconds with `met.py apart`. Their groups test `src/gpu`, and `src/gpu` and `src/screen`. |
| `uses/crash.py` | A program that holds the lock of `gpu` in another process, kills that process or not, and then tries the lock. It writes `free` if it gets the lock, and `taken` if not. |

The cases of the parts run `test.py` on `.toolchain/tests/data/build/family`, as `.toolchain/tests/docs/build.toml.md` tells, or on `.toolchain/tests/data/test/parted`.
`parted` has the parts `alpha` and `beta`, each with a program and a group. The folder of `beta` is `deep/beta`.
The cases of `alpha` reach both sides of its condition. The case of `beta` reaches one side, and keeps one block of memory.
The project exempts that side and that block, so a run of `alpha` meets two exemptions of a different part.

| Case | Claim | False variant |
| --- | --- | --- |
| a script | The script waits for `? name`, puts `note.txt` and types `you`. The lines come in order, and the file is there. | The script types `nobody`, and puts no file. |
| a helper | The command writes the line that the helper wrote into a file. | No helper. |
| a variable of the environment, given | `env` gives `C23_SAID` the value `port {port}`. | No `env`. |
| a variable of the environment, taken away | `env` removes `ZIG_LOCAL_CACHE_DIR`, thus the command writes `unset`. | No `env`. |
| claims on the status and on the output | `stdin` gives `two`. The command writes `one two`, and ends with 3. `status`, `status_not`, `has` and `lacks` hold. | `stdin` gives `three`. |
| a script that removes a file | The script removes `gone.txt` that `files` wrote, thus the command writes `False`. | The script removes no file. |
| a folder of files | `folders` copies `note.txt` into `{case}/in`. | The folder is empty. |
| a script that sends an interrupt | The script waits for `ready`, sends an interrupt, and waits for `got`. The output has `got interrupt`, then `done`. | The script sends a hang-up. |
| a script that sends a termination | The output has `got termination`, then `done`. | The script sends an interrupt. |
| a script that sends a hang-up | The output has `got hang-up`, and no `done`. | The script sends an interrupt. |
| an interrupt that the command ignores | `ignore` is `["interrupt"]`, so the output has no `got interrupt`. | `ignore` is empty. |
| a script that closes the output | The script closes the output after `ready`, thus `signals.py` ends with 3. | The script closes nothing. |
| a step with no wait that pauses | The second step has no `wait`, and pauses 2 seconds. The output has `paused`. | No second step. |
| a case with no false variant | `test` stops: `the case alone has no false variant`. | `passes.toml` in place of `alone.toml`. |
| a case that claims nothing | `test` stops: `the case silent claims nothing`. | `passes.toml`. |
| a case with a key that no case has | `test` stops: `a case has no key colour`. | `passes.toml`. |
| a signal that is not known | `test` stops: `the case unknown sends stop`. | `passes.toml`. |
| a close of the input | `test` stops: `the case input closes input`. | `passes.toml`. |
| a pause of no time | `test` stops: `the case zero pauses 0`. | `passes.toml`. |
| an ignored termination | `test` stops: `the case deaf ignores ['termination']`. | `passes.toml`. |
| an interrupt and a termination in one script | `test` stops: `the case both sends an interrupt and a termination`. | `passes.toml`. |
| a signal after a hang-up | `test` stops: `the case after sends a signal after a hang-up`. | `passes.toml`. |
| a wait after a close of the output | `test` stops: `the case blind waits for a line after it closes the output`. | `passes.toml`. |
| a case that differs | `test` writes `fails: differs`, the status and the output. Then it stops: `not as written: fails`. | `passes.toml`. |
| a case that differs, with a byte in its output that is not text | `test` writes `bytes: differs` and the output, with the character U+FFFD in place of the byte. Then it stops: `not as written: bytes`. | `passes.toml`. |
| a case that does not end in time | `test` writes `late: did not end in 2 seconds`, and stops. | `passes.toml`. |
| a rule of the tests | The group `held/said` fails, and the group `free/said` passes. | `passes.toml` in `held`. |
| no case | `test` writes `no case: tests/cases holds no case`, and ends with 0. | `passes.toml`. |
| a false variant that still holds | `test --break` stops: `still as written with their claims made false: still`. | `passes.toml`. |
| a target that does not run here | `nowhere/project.toml` is the project. `test --target nowhere` stops: `nowhere does not run here`. | No `--target`. |
| a case that needs what is not linked | `test` writes `compiled, not linked: later:`. Then it stops: `the cases need what is linked: later`. | `linked.txt` is there. |
| the output of the cases | `test` runs the case `said`, and `{case}/out/{target}/said.txt` holds its output `ended after`. | `test --break`, which writes no `said.txt`. |
| a claim of a pattern | The output matches `first.*second: \d+` over two lines. | The two lines in the other order. |
| a claim of a pattern that is not found | The output has `hop A` one time, and the claim refuses `hop A.*hop A`. | The output has `hop A` two times. |
| a claim of the whole output | The output is the same as `.toolchain/tests/data/test/output.txt`. | The output lacks its second line. |
| copies of a case | `test --copies 3` runs 3 copies of `ran.toml`; the third copy writes `cases/ran/0/2/ran.txt`. | No `--copies`, thus one copy and no folder `2`. |
| a case that runs alone | With `--copies 3`, the case `lone` (`alone = true`) runs one time, in `cases/lone/0`. | `ran.toml` in place of `lone.toml`. |
| copies that differ | `test --copies 2` on `fails.toml` writes `fails: differs in 2 of 2 copies`. | No `--copies`. |
| rounds of the cases | `test --rounds 2` writes `round 2 of 2`. | No `--rounds`. |
| the cases whose name holds a text | `test -k second` runs `second case` of `two.toml`, and not `first case`. | `-k first`. |
| a text that no name holds | `test -k nothing` stops: `no case has nothing in its name`. | `-k second`. |
| a project with no copies | The `.toolchain/project.toml` of the project has no `[test] copies`: `test` stops. | The project gives `copies = 1`. |
| a case that holds no port gets no port | The case `unported` holds no `{port}`, so `{address}` has no value: `test` stops with `no variable {port} for 127.0.0.1:{port}`. | `ported.toml`, which names `{port}`. |
| the groups of a part | `test --part alpha` on `family` runs the group `alpha/alpha`, and not `beta/beta`. | `--part beta`. |
| the groups of a part in a deep folder | `test --part beta` on `parted` runs the group `deep/beta/beta`, and not `alpha/alpha`. | `--part alpha`. |
| a part with no group | `test --part gamma` on `family` stops: `no case group is in the parts gamma`. | `--part alpha`. |
| the branches of a part | `test --branches --part alpha` on `parted` probes only `alpha`, and does not read the exemption of `beta`: `branches: 3 outcomes, 3 reached`. | No `--part`: 6 outcomes. |
| the leaks of a part | `test --leaks --part alpha` on `parted` runs the 2 cases of `alpha`, and does not read the exemption of `beta`: `leaks: 2 cases, 2 give back what they take`. | No `--part`: 3 cases. |
| a changed run makes each part after the parts that it uses | `test --branches` on `.toolchain/tests/data/build/ordered` builds `zeta.txt` before `alpha.txt`, and writes `branches: 0 outcomes, 0 reached`. | `unordered`: the link of `alpha.txt` is not there. |
| a named group runs alone | `test --group deep/beta/beta` on `parted` runs that group, and not `alpha/alpha`. | `--group alpha/alpha`. |
| a named group that is not there | `test --group nowhere` on `parted` stops: `no case group nowhere`. | `--group alpha/alpha`. |
| a table gives a verdict for each row | It writes `<row>: as written` for each of the 3 rows, and then `table: 3 cases: 3 as written`. | `table_ends.toml`. |
| the break run gives each row its false input | `test --break` writes `<row>, made false: fails, as it must` for each of the 3 rows. | `table_still.toml`. |
| a row whose false input still holds | `test --break` stops, and names the row. | `table.toml`. |
| a row that claims its whole answer | The 2 rows of `table_whole.toml` pass. The case writes the files `said/two.txt` and `said/one.txt`. | `said/two.txt` holds 1 line. |
| the break run of a row that claims its whole answer | `test --break` writes `table_whole: 2 claims made false: 2 cases failed`. | `said/two.txt` holds 1 line, which is the answer to the false input. |
| a whole answer that is not the text of the file | Each of the 3 rows of `table_whole_differs.toml` gets `differs`. | `passes.toml`. |
| a table whose command ends before its last row | The row at which the command ended, and the row after it, fail. `test` names the first one. | `table.toml`. |
| a table whose command gives more answers than rows | Each row fails: `is one of 3 rows, and the command gave 6 answers`. | `table.toml`. |
| a table whose inputs and answers are longer than a pipe holds | `long_table.py` gets `aaaa`, the text of each answer. `test` reads the answers while it writes the inputs, thus each row passes: `long: 60 cases: 60 as written`. | `long_table.py` gets `bbbb`, which no answer has. |
| a table that is longer than the timeout, with each row in time | The timeout is 2 seconds, and the 4 rows of `table_paced.toml` take 2.8 seconds. The time starts again at each answer, thus each row passes: `table_paced: 4 cases: 4 as written`. | `table_stalls.toml`, in which a row answers after 3 seconds. |
| a table whose rows need their order | The table passes in its order, and fails in the reverse order: `differs in the reverse order`. | `table.toml`. |
| a table whose command ends with another status | Each row fails: `is in a run that differs`. | `table.toml`. |
| a table with no row | `test` stops: `the table greet has no row`. | `passes.toml`. |
| a table with a false variant | `test` stops: `the table greet has rows, and a table has no key false`. | `passes.toml`. |
| a row with no false input | `test` stops: `a row of the table greet has no key false`. | `passes.toml`. |
| a row that claims a status | `test` stops: `a claim of a row has no key status`. | `passes.toml`. |
| a row that claims nothing | `test` stops: `the row greet writes the name that it gets claims nothing`. | `passes.toml`. |
| a table that claims nothing for its run | `test` stops: `the case greet claims nothing`. | `passes.toml`. |
| -k chooses the rows of a table | `test -k second` runs 1 row of `table.toml`: `table: 1 cases: 1 as written`. | `-k greet`, which runs the 3 rows. |
| a case with no reason for its own process, in a project with tables | `test` stops: `the case passes has its own process and states no reason`. | The project with no `tables`. |
| a case that states the reason of its own process | With `tables`, `stated: as written` and `fed: as written`. | `passes.toml`, which states no `process`. |
| a process that is no reason | `test` stops, also with no `tables`: `the case worded states the process speed`. | `own_stated.toml`. |
| a case that states the process script, with no script and no standard input | `test` stops, also with no `tables`: `the case silent states the process script, and it has no script and no stdin`. | `own_stated.toml`. |
| a table that states a process, in a project with tables | `test` stops: `the table greet states process`. | The project with no `tables`. |
| 3 cases that refuse the calls of one function by hand, in a project with tables | `test` stops: `3 cases refuse the calls of malloc one after the other, from the case refused 1: write a sweep`. | `own_stated.toml`. |
| a pattern of folders that matches no file stops the run | In the project of `uses/one/project.toml` with the group `patterned.toml`, `test` stops: `data/*.txt: no file matches the pattern`. | The file `{case}/data/a.txt` is there. |
| a group waits for the lock of its use | `locks.py` holds `gpu` in a helper, and `test` writes `drawn: waits for the use gpu, which another run holds`, then `drawn: 1 cases: 1 as written`. | The helper holds `display`. |
| a group with no use runs while a use is held | The helper holds `gpu`, and `plain` passes with no line of a wait. | The group `drawn`. |
| a group takes its uses in the order of their names | The helper holds `display` and `gpu`. `both` waits for `display`, and not for `gpu`. | The helper holds only `gpu`. |
| a group holds the lock of its use while its cases run | `probe` writes `taken`. | `uses/nouse`: no lock is taken. |
| a group gives the lock of its use back after its cases | `drawn` and `both` pass in 1 run. | Only `drawn`. |
| a use with no pattern stops the run | `[test] uses: gpu has no pattern`. | `uses/one`. |
| a pattern of a use that matches no file stops the run | `[test] uses: src/none/** matches no file`. | `uses/one`. |
| the cases of a group run at the same time | With `--workers 2`, the 2 cases of `met.toml` see each other: `met: 2 cases: 2 as written`. | `--workers 1`: `a meets b` waits 5 seconds alone, and fails. |
| 2 groups that share a use take turns in 1 run | With `--workers 2`, `apart_one` and `apart_two` share `gpu`, so their cases do not see each other. No line of a wait comes, since only 1 run holds the locks. | `uses/nouse`: the 2 cases run at the same time, and see each other. |
| the groups write their verdicts in their order | With `--workers 2`, `quick` ends first, and the output still holds `slow`, `order_1`, `quick` and `order_2` in this order. | Only `order_2.toml`. |
| a file of the build folder is placed by a link | The folder of the build holds `prog.txt`, and `linked` writes `True`: `linked: as written`. | `copied.toml`: a copy is not the same file. |
| a file of a case does not write into a linked file | After `overwritten`, `{case}/out/prog.txt` still holds `p`. | `overwrote.toml` writes into the build output. |
| a count of 0 workers stops the run | `--workers 0`: `[test] workers and --workers are a count of 1 or more`. | `--workers 1`. |
| a run that is killed gives its lock back | `crash.py` kills the process that holds `gpu`, and writes `free`. | The process is not killed: `taken`. |
