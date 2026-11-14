# .toolchain/tests/cases/workflows.toml

The group `workflows` checks `.toolchain/tools/workflows.py`.
The first case checks the workflows of the template.
The other cases write a small project into `{case}/p` with `files`: `.toolchain/project.toml` and one workflow.

| Case | Claim | False variant |
| --- | --- | --- |
| the workflows of the template | `workflows.py` finds no fault in the 5 workflows of the template: `no fault in 5 workflows`. | A project whose `ci.yml` lacks the target `aarch64-windows-gnu`. |
| a host that a workflow does not run on | A project of 6 targets, and a `ci.yml` with only the Linux host: `.github/workflows/ci.yml: the matrix does not run on x86_64-windows-gnu`. | A `ci.yml` with the 2 hosts. |
| a name that is not a host | A `ci.yml` with the 2 hosts and `aarch64-macos`, a target that is no host: `.github/workflows/ci.yml: aarch64-macos is not a host of the project`. | The 2 hosts only. |
| a workflow with no matrix | A `cla.yml` with no line `- target:` makes no fault. | The file gets the line `- target: x86_64-linux-gnu`, so its matrix lacks 5 targets. |
