# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import fnmatch
import re

import shared
from style import CONFIG, ROOT, ours

OLDER = [
    (r'\bNULL\b', 'nullptr'),
    (r'#\s*include\s*<stdbool\.h>', 'nothing: bool, true and false are keywords'),
    (r'\b_Bool\b', 'bool'),
    (r'\b_Alignof\b', 'alignof'),
    (r'\b_Alignas\b', 'alignas'),
    (r'\b_Static_assert\b', 'static_assert'),
    (r'\b_Thread_local\b|\bTHREAD_LOCAL\b', 'thread_local'),
    (r'\b_Noreturn\b', '[[noreturn]]'),
    (r'\b__attribute__\b|\b__declspec\b', 'an attribute in brackets: [[gnu::...]], [[clang::...]]'),
    (r'\benum\s*\{', 'a named enum with its width: enum name : uint32_t {'),
    (r'\benum\s+\w+\s*\{', 'the enum with its width stated: enum name : uint32_t {'),
    (r'\(void\)\s*[A-Za-z_]\w*\s*;', '[[maybe_unused]] where the parameter is declared'),
    (r'=\s*\{\s*0\s*\}\s*;', '= {}'),
    (r'^[ \t]*#[ \t]*define[ \t]+\w+[ \t]+[-+(]*(?:0[xX][0-9a-fA-F]|[0-9])', 'a typed constexpr'),
]

SILENT = re.compile(r'''/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*\'''', re.S)


def excused(paths, faults):
    listed = [[entry.get('path', ''), entry.get('why'), 0] for entry in CONFIG.get('c23', {}).get('exception', [])]
    kept = []
    for path in paths:
        mine = [entry for entry in listed if fnmatch.fnmatch(path, entry[0])]
        for entry in mine:
            entry[2] += len(faults.get(path, []))
        if not mine:
            kept += faults.get(path, [])
    for where, why, used in listed:
        if not why:
            kept.append(".toolchain/project.toml:1: the exception for '%s' states no reason" % where)
        elif not used:
            kept.append(".toolchain/project.toml:1: the exception for '%s' excuses nothing" % where)
    return kept


def main():
    paths, found = [path for path in ours() if not path.startswith('third_party/')], {}
    for path in paths:
        text = (ROOT / path).read_text(encoding='utf-8')
        code = SILENT.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text)
        for older, newer in OLDER:
            for m in re.finditer(older, code, re.M):
                line = code.count('\n', 0, m.start()) + 1
                found.setdefault(path, []).append('%s:%d: %s  ->  %s' % (path, line, m.group(0).strip(), newer))
    shared.report(excused(paths, found), len(paths))


if __name__ == '__main__':
    main()
