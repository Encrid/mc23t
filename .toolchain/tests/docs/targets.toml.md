# .toolchain/tests/cases/targets.toml

The group `targets` checks the key `targets` of `[project]`: `.toolchain/docs/project.toml.md`, *[project]*.
Each case writes a small project into `{case}/p` with `files`: `.toolchain/project.toml`, and for some cases one workflow.
`workflows.py` reads the configuration first, so its faults of the key come before any check of a workflow.

| Case | Claim | False variant |
| --- | --- | --- |
| a project that states no targets | `[project]` has no `targets`: `workflows.py: .toolchain/project.toml: write the targets of the project in [project] targets`. | `targets = ["x86_64-linux-gnu"]`. |
| a target that the toolchain does not have | The list holds `riscv64-linux-gnu`: `workflows.py: [project] targets: riscv64-linux-gnu is not a target of the toolchain`. | The list holds only `x86_64-linux-gnu`. |
| a target named 2 times | The list holds `x86_64-linux-gnu` 2 times: `workflows.py: [project] targets: x86_64-linux-gnu comes 2 times`. | The name 1 time. |
| a build for a target outside the list of the project | A project of the 2 targets of x64 Windows and Linux: `build --target aarch64-macos` stops with `build.py: no target aarch64-macos; the targets: x86_64-windows-gnu x86_64-linux-gnu`. | The list also holds `aarch64-macos`. |
| a matrix with a target outside the list of the project | A project of the same 2 targets, and a `ci.yml` that also names `aarch64-macos`: `.github/workflows/ci.yml: aarch64-macos is not a host of the project`. | A `ci.yml` with the 2 targets. |
| the matrix of toolchain.yml names each target of the toolchain | A project of the same 2 targets, and a `toolchain.yml` with the 6 targets: `no fault in 1 workflows`. | A `toolchain.yml` with the 2 targets: it lacks 4 targets of the toolchain. |
