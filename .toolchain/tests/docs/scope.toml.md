# .toolchain/tests/cases/scope.toml

The group `scope` checks `.toolchain/tools/scope.py`.
Each case writes the list of the changed paths into `{case}/changed.txt` with `files`, and gives it to `scope.py` with `--changed`.
The paths of the lists need not be there, since `scope.py` reads only their text. Only a config file and the case files must be there.
Each case file of the data holds one case, which no case runs.

| Data | Content |
| --- | --- |
| `parted` | The parts `a`, `b`, which uses `a`, and `deep`, with the folder `a/deep`. The file `.toolchain/config/c.toml` states the part `c`, and `checks.toml` states no part. Each part has one group in its folder, and the part `b` has also the group `b/more`. The group `all` is in no part, and states `whole = true`. |
| `grouped` | A project with no part. The group `store` states `code = ["src/store/**", "tests/store/**"]`, and the group `whole` states `whole = true`. |
| `mono` | A project with no part. Its groups `one` and `two` state no key. |
| `owned` | A project with no part. Its one group `x` states `code = ["src/x/**"]`. |
| `miscoded` | A project whose group states `code = "src/x"`. |
| `miswhole` | A project whose group states `whole = "yes"`. |
| `plain` | A project with no part and no case group. |

| Case | Claim | False variant |
| --- | --- | --- |
| a source of a part names the groups of that part only | `src/a/x.c` gives `--group a/a`, and not the group of `b`, which uses `a`. | `src/b/y.c`. |
| a nested folder names the groups of its own part | `src/a/deep/x.c` gives `--group a/deep/deep`, the part of the longest folder. | `src/a/x.c`. |
| the config file of a part names the groups of the part | `.toolchain/config/c.toml` gives `--group c/c`. | `checks.toml`. |
| a case file names its own group | `tests/cases/b/b.toml` gives `--group b/b`, and not the group `b/more` of the same part. | The file of the group `all`. |
| a group of the whole does not run for a changed source | `src/b/y.c` gives the 2 groups of `b`, and not the group `all`. | A tool of the toolchain. |
| a group names the code that it tests | In `grouped`, `src/store/a.c` and `tests/store/main.c` give `--group store`. | The file of the group `whole`. |
| a project of one piece names each group for a changed source | In `mono`, a source and a config file give `--group one --group two`. | A readme. |
| a file of the toolchain names the groups of the whole | `.toolchain/tools/build.py` and `.toolchain/toolchain.toml` give `--group all`. | A document of the toolchain. |
| a file of the toolchain names no group in a project with no group of the whole | In `mono`, `.toolchain/tools/build.py` and `project.py` write nothing. | A source. |
| a document and a workflow name no group | A readme, 2 documents of a part, a workflow and a document of the toolchain write nothing. | A source of `b` too. |
| a pull request into main names the groups of the whole | `--into main` gives `--group all`. | `--into dev`. |
| a pull request into main names no group in a project with no group of the whole | In `mono`, `--into main` writes nothing. | `--into dev`. |
| a project with no case group names nothing | The project `plain` writes nothing. | The project `parted`. |
| an empty list names nothing | No path writes nothing. | A source of `b`. |
| a source that no group tests stops the tool | In `owned`, `src/y/a.c` stops the tool: `src/y/a.c: no case group tests this file`. | `src/x/a.c`. |
| a code that is no list of patterns | In `miscoded`, the tool stops: `tests/cases/x.toml: code is a list of patterns`. | The project `owned`. |
| a whole that is not true or false | In `miswhole`, the tool stops: `tests/cases/x.toml: whole is true or false`. | The project `mono`. |
| a list that is not there stops the tool | `cannot read the list <path>`. | The list is there. |
