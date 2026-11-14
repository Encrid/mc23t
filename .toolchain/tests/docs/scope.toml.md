# .toolchain/tests/cases/scope.toml

The group `scope` checks `.toolchain/tools/scope.py`.
Each case writes the list of the changed paths into `{case}/changed.txt` with `files`, and gives it to `scope.py` with `--changed`.
The paths of the lists need not be there, since `scope.py` reads only their text. Only a config file must be there.

| Data | Content |
| --- | --- |
| `parted` | The parts `a`, `b`, which uses `a`, and `deep`, with the folder `a/deep`. The file `.toolchain/config/c.toml` states the part `c`, and `checks.toml` states no part. |
| `plain` | A project with no part. |

| Case | Claim | False variant |
| --- | --- | --- |
| a source of a part names the part and each part that uses it | `src/a/x.c` gives `--part a --part b`. | `src/b/y.c`. |
| a source of a part that no part uses names only that part | `src/b/y.c` gives `--part b`. | `src/a/x.c`. |
| a nested folder names its own part | `src/a/deep/x.c` gives `--part deep`, the part of the longest folder. | `src/a/x.c`. |
| the readme and the config file of a part name the part | `docs/usage/c.md` and `.toolchain/config/c.toml` give `--part c`. | A source of `b` too. |
| a case group and a document of a part name the part | A case file, a document and a header of `b` give `--part b`. | A case file of no part. |
| a file of no part gives the whole project | `readme.md` beside a source of `b` writes nothing. | Only the source of `b`. |
| a config file of no part gives the whole project | `checks.toml` writes nothing. | `c.toml`. |
| a pull request into main gives the whole project | `--into main` writes nothing. | `--into dev`. |
| a project with no part gives the whole project | The project `plain` writes nothing. | The project `parted`. |
| an empty list gives the whole project | No path writes nothing. | A source of `b`. |
| a list that is not there stops the tool | `cannot read the list <path>`. | The list is there. |
