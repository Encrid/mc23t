# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import shutil
import subprocess
import sys
from pathlib import Path

import area
import host

RUNS = {'build': [], 'branches': ['--branches'], 'leaks': ['--leaks'], 'fail': ['--branches']}


def ran(tools, tool, project, more):
    done = subprocess.run([sys.executable, str(Path(tools) / tool), '--root', project] + more,
                          capture_output=True, text=True)
    return [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]


def built(tools, project, out, run, picked):
    folder = Path(out) / run
    tool = 'build.py' if run == 'build' else 'test.py'
    shutil.rmtree(folder, ignore_errors=True)
    said = ran(tools, tool, project, ['--out', str(folder)] + RUNS[run] + (['-k'] + picked if picked else []))
    modules = sorted(folder.glob('**/probe.wasm'), key=lambda path: len(path.parts))
    return said, modules[0] if modules else None


def planned(tools, project, out, words):
    module = Path(out) / 'fail' / 'module.wasm'
    if not module.is_file():
        said, found = built(tools, project, out, 'fail', [])
        if not found:
            print('\n'.join(said))
            return
        shutil.copyfile(found, module)
        module.with_suffix('.txt').write_text(found.parent.name, encoding='utf-8')
    target = module.with_suffix('.txt').read_text(encoding='utf-8')
    part = ''.join(word[5:] for word in words if word.startswith('part:'))
    failed = ''.join(' ' + word for word in words if not word.startswith('part:'))
    host.run(Path(project) / 'build' / 'third_party' / 'bb_wasm' / target, module, failed, part)


def answered(tools, project, out, words):
    run, picked = words[0], words[1:]
    if run == 'fail':
        return planned(tools, project, out, picked)
    said, module = built(tools, project, out, run, picked)
    for line in said:
        if line.startswith('stand_in: ') or line is said[-1]:
            print(line)
    if module:
        area.shown(module.read_bytes())


def main():
    tools, project, out = sys.argv[1:4]
    said = ran(tools, 'fetch.py', project, [])
    if not said or not said[-1].endswith(('zig', 'zig.exe')):
        print('\n'.join(said), flush=True)
    for line in sys.stdin:
        answered(tools, project, out, line.split())
        print('', flush=True)


if __name__ == '__main__':
    main()
