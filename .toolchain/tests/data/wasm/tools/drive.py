import shutil
import subprocess
import sys
from pathlib import Path

import area

RUNS = {'build': [], 'branches': ['--branches'], 'leaks': ['--leaks']}


def ran(tools, tool, project, more):
    done = subprocess.run([sys.executable, str(Path(tools) / tool), '--root', project] + more,
                          capture_output=True, text=True)
    return [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]


def answered(tools, project, out, words):
    run, picked = words[0], words[1:]
    folder = Path(out) / run
    tool = 'build.py' if run == 'build' else 'test.py'
    shutil.rmtree(folder, ignore_errors=True)
    said = ran(tools, tool, project, ['--out', str(folder)] + RUNS[run] + (['-k'] + picked if picked else []))
    if said:
        print(said[-1])
    modules = sorted(folder.glob('**/probe.wasm'), key=lambda path: len(path.parts))
    if modules:
        area.shown(modules[0].read_bytes())


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
