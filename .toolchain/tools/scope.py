# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import fnmatch
import subprocess
import sys
import tomllib

from shared import arguments, base, config, die, part_of, repository

TOPS = ('src/', 'include/', 'tests/')
CONFIG = '.toolchain/config/'
CODE = TOPS + ('tools/',)
BUILT = (CONFIG, '.toolchain/tools/', '.toolchain/runtime/')
PROJECT = '.toolchain/project.toml'
FILES = ('.toolchain/toolchain.toml', PROJECT, '.toolchain/graph.zig', 'project.py')
CHECKED = ('check', 'dup', 'prose', 'style')


def stated(root, path):
    try:
        found = tomllib.loads((root / path).read_text(encoding='utf-8')).get('parts', {})
    except (OSError, ValueError):
        return None
    return next(iter(found)) if len(found) == 1 else None


def owner(settings, root, path):
    if path.startswith(CONFIG):
        return stated(root, path)
    top = next((top for top in TOPS if path.startswith(top)), None)
    return part_of(settings, path[len(top):]) if top else None


def git(root, *argv):
    done = subprocess.run(['git', '-C', str(root)] + list(argv), capture_output=True)
    return None if done.returncode else done.stdout


def versions(root, path, into):
    if not repository(root):
        return None
    shared = base(root, into)
    before = shared and git(root, 'show', shared + ':' + path)
    if not before:
        return None
    try:
        return [tomllib.loads(text) for text in (before.decode('utf-8'), (root / path).read_text(encoding='utf-8'))]
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def checked_only(root, into):
    tables = versions(root, PROJECT, into)
    if not tables:
        return False
    kept = [{name: value for name, value in table.items() if name not in CHECKED} for table in tables]
    return kept[0] == kept[1]


def failed_only(root, path, into):
    tables = versions(root, path, into) if path.startswith(CONFIG) else None
    if not tables:
        return None
    calls = [table['fail'].pop('calls', None) if isinstance(table.get('fail'), dict) else None for table in tables]
    if tables[0] != tables[1] or not all(isinstance(one, dict) for one in calls):
        return None
    return sorted(name for name in calls[0].keys() | calls[1].keys() if calls[0].get(name) != calls[1].get(name))


def calling(root, names):
    if not names:
        return []
    done = subprocess.run(['git', '-C', str(root), 'grep', '-l', '-z', '-w', '-F', '--untracked']
                          + [item for name in names for item in ('-e', name)], capture_output=True)
    if done.returncode > 1:
        die('git grep fails in %s: %s' % (root, done.stderr.decode('utf-8', 'replace').strip()))
    return [path for path in done.stdout.decode('utf-8').split('\0') if path and not path.startswith(CONFIG)]


def groups(settings, root):
    folder = root / settings.get('test', {}).get('cases', 'tests/cases')
    found = []
    for path in sorted(folder.rglob('*.toml')):
        table = tomllib.loads(path.read_text(encoding='utf-8'))
        file, code, whole = path.relative_to(root).as_posix(), table.get('code'), table.get('whole', False)
        if code is not None and not (isinstance(code, list) and all(isinstance(item, str) for item in code)):
            die('%s: code is a list of patterns' % file)
        if not isinstance(whole, bool):
            die('%s: whole is true or false' % file)
        if table.get('case'):
            name = path.relative_to(folder).with_suffix('').as_posix()
            found.append({'name': name, 'file': file, 'code': code, 'whole': whole, 'part': part_of(settings, name)})
    return found


def tests(settings, root, found, group, path):
    if path in [other['file'] for other in found]:
        return path == group['file']
    if group['code'] is not None:
        return any(fnmatch.fnmatch(path, pattern) for pattern in group['code'])
    if group['whole']:
        return False
    built = path.startswith(CODE + (CONFIG,)) or path == PROJECT
    return built and owner(settings, root, path) == group['part']


def claimed(settings, root, names):
    found = groups(settings, root)

    def measured(path):
        testers = [group['name'] for group in found if tests(settings, root, found, group, path)]
        return bool(testers) and all(name in names for name in testers)
    return measured


def scoped(settings, root, paths, into):
    found = groups(settings, root)
    wholes = [group['name'] for group in found if group['whole']] or [group['name'] for group in found]
    if not found:
        return wholes
    picked = set(wholes) if into == 'main' else set()
    for path in paths:
        if path == PROJECT and checked_only(root, into):
            continue
        mine = [group['name'] for group in found if tests(settings, root, found, group, path)]
        if not mine and path.startswith(CODE):
            die('%s: no case group tests this file' % path)
        if not mine and (path.startswith(BUILT) or path in FILES):
            mine = wholes
        names = failed_only(root, path, into) if mine else None
        if names is not None:
            callers = calling(root, names)
            mine = [group['name'] for group in found if group['name'] in mine
                    and any(tests(settings, root, found, group, caller) for caller in callers)]
        picked.update(mine)
    return sorted(picked)


def main():
    args = arguments('--changed', '--into')
    if not args.changed:
        die('name the list of the changed paths with --changed')
    try:
        text = open(args.changed, encoding='utf-8').read()
    except OSError:
        die('cannot read the list %s' % args.changed)
    paths = [line.strip().replace('\\', '/') for line in text.splitlines() if line.strip()]
    found = scoped(config(args.root), args.root, paths, args.into)
    if found:
        sys.stdout.buffer.write((' '.join('--group %s' % group for group in found) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
