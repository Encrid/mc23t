# .toolchain/tools/scope.py

`scope.py` gives the case groups that test the files that a pull request changes. The step `Gate` of `ci.yml` runs each gate only for these groups: `.toolchain/docs/workflows.py.md`, *The jobs of ci.yml*.

```sh
python .toolchain/tools/scope.py --changed <file> --into <branch>
```

`--changed` names a file with one changed path on each line, as `git diff --name-only` writes them. `--into` names the branch that the pull request goes into.
The tool writes one line with `--group <group>` for each group, in the order of the names. If no group tests the change, it writes nothing.

## The code of a group

A test belongs to the code that it tests. A group states that code with the key `code`, at the top of its file:

```toml
code = ["src/store/**", "tests/store/**"]
```

Each item is a pattern for a path of the project, with `*` for any text.
A group tests a path that one of its patterns matches. It also tests its own file, and no other group tests that file by default.

A group with no `code` has a default:

1. In the folder of a part, it tests the files of that part.
2. In no part, it tests the project as a whole.

The files of a part are its sources, its headers, its tests and its config file. Its documents do not count.
A config file belongs to the part whose table `[parts.<part>]` it states alone.

## The scope

For a pull request into a different branch than `main`, each changed path gives the groups that test it.
A path of the build that no group tests gives the groups of the whole, since only the whole tests it.
The paths of the build are the files of `src`, `include`, `tests` and `tools`, the files of `.toolchain/config`, and the copy of the toolchain.
Each other path gives no group: a document and a workflow change no code.

A part that uses a changed part gives no group. Its groups test its own code.

For a pull request into `main`, the tool gives the groups of the whole.

The tool stops with these faults:

- `name the list of the changed paths with --changed`.
- `cannot read the list <path>`.
- `<group file>: code is a list of patterns`.
- `<path>: no case group tests this file`, for a path of the build in a project where each group states its code.
- `no case group tests the project as a whole`, for a pull request into `main` of such a project.

A project with no case group gives nothing.

## Functions

| Function | Result |
| --- | --- |
| `main()` | Reads the options and the list, and writes the line. |
| `scoped(settings, root, paths, into)` | Gives the sorted names of the groups of the scope. |
| `groups(settings, root)` | Gives each group of `[test] cases` that has a case: its name, its file, its `code` and its part. |
| `whole(group)` | Tells if a group tests the project as a whole. |
| `tests(settings, root, group, path)` | Tells if a group tests a path. |
| `claimed(settings, root, names)` | Gives the function that tells if the named groups measure a file: `.toolchain/docs/branches.py.md`, *The files of the named groups*. |
| `owner(settings, root, path)` | Gives the part of one path, or `None`. |
| `stated(root, path)` | Gives the part that a config file states alone, or `None`. |
