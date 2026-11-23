# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import fetch
import shared

case, where = Path(sys.argv[2]).resolve(), sys.argv[3]
main = case / 'main'
main.mkdir(parents=True)
git = ['git', '-c', 'user.name=case', '-c', 'user.email=case@example.com', '-c', 'commit.gpgsign=false']
subprocess.run(git + ['init', '-q'], cwd=main, check=True)
subprocess.run(git + ['commit', '-q', '--allow-empty', '-m', 'case'], cwd=main, check=True)
if where == 'worktree':
    subprocess.run(git + ['worktree', 'add', '-q', '--detach', str(case / 'tree')], cwd=main, check=True)
    shared.HERE = case / 'tree'
if where == 'inner':
    (main / 'inner').mkdir()
    shared.HERE = main / 'inner'
print(fetch.archives({'archives': 'build/archives'}).relative_to(case).as_posix())
