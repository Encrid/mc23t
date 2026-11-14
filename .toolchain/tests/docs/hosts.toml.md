# .toolchain/tests/cases/hosts.toml

The group `hosts` checks `.toolchain/tools/hosts.py`.
Each case writes `.toolchain/project.toml` of a project `p` into `{case}` with `files`, and names a host with `--host`.
Each machine gives the same output for a named host, so each case gives the same output on each machine.

| Case | Claim | False variant |
| --- | --- | --- |
| a host builds itself and each target that names it | A project of 6 targets: the Linux host writes `x86_64-linux-gnu`, `aarch64-macos`, `aarch64-linux-gnu` and `x86_64-macos`, in the order of `[targets]`, and no target of Windows. | The Windows host. |
| a host of a project with the 2 x64 targets builds only itself | The Windows host writes only `x86_64-windows-gnu`. | A project of 6 targets, so it also writes `aarch64-windows-gnu`. |
| a name that is not a host stops the tool | `--host aarch64-macos`: `aarch64-macos is not a host of the project`. | The Linux host. |
| a target that a project adds with no built_on is its own host | The project adds `[targets.riscv64-linux-gnu]` with no `built_on`. The host `riscv64-linux-gnu` writes it. | The Linux host, which does not build it. |
