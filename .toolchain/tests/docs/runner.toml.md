# .toolchain/tests/cases/runner.toml

The group `runner` checks `.toolchain/tools/runner.py`.
Each case writes `.toolchain/project.toml` into `{case}` with `files`, and copies 1 needs file of `.toolchain/tests/data/runner/<set>/needs.toml` into `{case}/.toolchain/config` with `folders`. Then it runs `runner.py --root {case}` for a named target.
A case cannot install a package or download an archive on each machine. Thus each case checks the commands that `runner.py` writes, and runs none of them.
Each machine writes the same commands for a named target. So each case gives the same output on each machine.
The needs of the cases are made up: no name of a real need, so the group stays free of every field.

| Case | Claim | False variant |
| --- | --- | --- |
| a project with no needs gives no command | `runner.py` writes nothing. | The project needs `alpha`. |
| the packages of each need in one install, then the commands of each need | On Linux, 1 sorted install holds the packages of the 2 needs, then the commands of each need come in the order of `[ci] needs`. | The project needs only `alpha`. |
| the brews of each need in one install on macOS | On macOS, 1 brew install holds the brews of the 2 needs, and the Linux tables give nothing. | The Linux target. |
| an archive for x86_64 of Windows, with the values of the cpu and the folders of the member dropped | The 2 archives of `beta` share 1 folder. The url and the digest take the texts of `AMD64`. The member drops its folder. The commands come last. | The `arm64` target. |
| an archive for arm64 of Windows takes the other row of values | The url and the digest take the texts of `ARM64`. | The project needs `alpha`, which Windows does not serve. |
| an archive unpacks with plain tar on Linux | The folder, the download, the check and the unpack use plain paths and `tar`. | The macOS target, which the need does not serve. |
| a need that is not declared | `[ci] needs: sound is not a need: alpha beta gamma second`. | The project needs `alpha`. |
| a placeholder with no text for the cpu of the target | The values hold only `AMD64`, and the target is `arm64`: `no variable .part.`. | The `x86_64` target. |
| the members of an archive drop different counts of folders | The members hold 1 member in a folder and 1 member at the top: the message of the 2 counts. | The needs file of the set `full`. |
| a target that runs on no machine | `--target nowhere`: `no machine runs the target nowhere`. | The target `x86_64-linux-gnu`. |

The workflows run the commands for real: the projects that state needs prove them on each runner.
