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
| `alone.toml` | The case `alone`, which has no false variant. |
| `silent.toml` | The case `silent`, which claims nothing. |
| `colour.toml` | The case `colour`, which has the key `colour`. |
| `signals.py` | A program that writes `ready`, reads a line, and writes `done`. It writes `paused` before `done` if 1 second went by after `ready`. |
| `signals.py`, the signals | For each signal, `signals.py` writes `got <signal>`. After a hang-up it ends with 0. If it cannot write `done`, it ends with 3. |
| `unknown_signal.toml`, `closed_input.toml`, `zero_pause.toml` and `ignored_termination.toml` | Each has one case with a value that a script or `ignore` does not allow. |
| `interrupt_termination.toml`, `after_hang_up.toml` and `wait_after_close.toml` | Each has one case with a script that cannot run the same way on each system. |
| `late.toml` and `late/project.toml` | The case `late`, which waits 9 seconds, and a timeout of 2 seconds. |
| `said.toml` and `ruled/project.toml` | The case `said`, which writes `ended after`, and a rule that refuses this text, but not in the group `free/said`. |
| `still.toml` | The case `still`, whose false variant also passes. |
| `later/project.toml` | An artifact that links `linked.txt`, which is not there. Its kind has `unlinked` steps. |
| `nowhere/project.toml` | The project of `.toolchain/project.toml`, and the target `nowhere`, whose `runs_on` is empty. |
| `port/project.toml`, `unported.toml` and `ported.toml` | A project whose variable `address` holds `{port}`. The case `unported` names `{address}` only, and the case `ported` names `{port}` too. |

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
