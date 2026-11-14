# .toolchain/tests/cases/fetch.toml

The group `fetch` checks `.toolchain/tools/fetch.py`.
Its cases run `fetch.py` or `build.py` on the project in `.toolchain/tests/data/fetch`, with the output in `{case}/out`.
That project has one source, `sample`: the archive `sample.zip` and the patch `.toolchain/tests/data/fetch/third_party/sample/<patch>.patch`.
The variable `patch` is `greeting`, the variable `top` is `sample`, and the variable `digest` is the digest of `sample.zip`.

The archive holds `sample/greeting.txt`. The patch `greeting` changes its line `hello` to `hello, patched`.
The patch `wrong` has a line of context that the file does not have.

| Case | Claim | False variant |
| --- | --- | --- |
| a source, patched | `fetch` patches `greeting.txt`, and the file holds `hello, patched`. | `--set patch=wrong`. |
| a patch that does not apply | With `--set patch=wrong`, `fetch` stops: `wrong.patch does not apply to greeting.txt`. | No `--set`. |
| an archive with no folder of its top | With `--set top=missing`, `fetch` stops: `fetch.py: sample: the archive has no folder missing`. | No `--set`: the top `sample` is in the archive. |
| a source that is not what its maker publishes | With a different digest, `fetch` stops: `sample.zip is not what the maker publishes`. | The digest of `sample.zip`. |
| a source that is not fetched | `build` stops: `sample is not fetched as project.toml states: run fetch`. | `fetch` in place of `build`. |
| a source that is fetched already | `fetched.txt` holds the stamp, thus `fetch` keeps `greeting.txt` as it is. | `fetched.txt` holds a different stamp. |
| a zip keeps the execute bits of its programs | `moded.py` writes `{case}/tools.zip`, fetches it with `fetched`, and writes `True`: `tool{exe}` can run. | `note.txt`, which has no execute bit. |
| a source with a folder for each target | After one `fetch`, a build for `aarch64-macos` and a build for `x86_64-linux-gnu` each copy `name.txt` of their own target. | `--set place=aarch64-macos`, so the two builds copy the file of `aarch64-macos`. |
| a source of the host is fetched one time | The project `tooled` is the project `hosted` with `host = true` on its source. Each host builds 2 targets, and `fetch` writes 1 folder with `fetched.txt`: `fetched 1`. | The project `hosted`: `fetched 2`. |
| a source of the host has the folder of the machine for each target | `homed.py` calls `sources` for each of the 2 targets that the machine builds, and the variable `{sample}` is 1 folder: `2 targets, 1 folders`. | The project `hosted`: `2 targets, 2 folders`. |
| a host that is not true or false | With `host = "yes"`, `fetch` stops: `fetch.py: sample: host is true or false`. | `host = true`. |
| a source of the host on a machine of no target | `homed.py` gives an empty `{home}` with its argument `nowhere`, and `sources` stops: `sample: a source of the host needs a machine of a target`. | No `nowhere`. |
| a host fetches a source for each target that it builds | The project `hosted` has 4 targets, and its source has an `into` for each target. Each host builds 2 of them, so `fetch` writes 2 folders with `fetched.txt`: `fetched 2`. | `--set place=one`, so the 2 targets share one folder: `fetched 1`. |

The case `a source with a folder for each target` uses the project in `.toolchain/tests/data/fetch/everywhere`.
Its source `everywhere` is `everywhere.zip`, with one digest. The zip holds `<target>/name.txt` for each of the 6 targets, and each file holds the name of its target.
The `top` of the source is the variable `place`, which is `{target}`.
The artifact `name.txt` copies `name.txt` from the folder of the source.

The case `a zip keeps the execute bits of its programs` runs `.toolchain/tests/data/fetch/moded.py`, which makes a zip with no network.
The zip records the mode 755 for `tool` and for `tool.exe`, and 644 for `note.txt`.
The program writes if the owner of the named file can run it.
On Linux and on macOS, `tool` keeps the execute bits of the zip. On Windows, the name `tool.exe` makes a program.

`.toolchain/docs/fetch.py.md` gives the limits of these cases.
The case `a host fetches a source for each target that it builds` uses the project in `.toolchain/tests/data/fetch/hosted`, and the archive `sample.zip` beside it.
The project in `.toolchain/tests/data/fetch/tooled` has the same 4 targets and the same source, with `host = true`.
The program `.toolchain/tests/data/fetch/homed.py` calls `sources` of `fetch.py` for each target that the machine builds. Then it writes the count of the targets and the count of the folders of `{sample}`.
