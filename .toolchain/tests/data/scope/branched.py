# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

at = sys.argv.index('--')
data, folder, added, command = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[at + 1:]
env = dict(os.environ, GIT_CONFIG_GLOBAL=str(folder.parent / 'none'), GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='c23', GIT_AUTHOR_EMAIL='c23@example.com',
           GIT_COMMITTER_NAME='c23', GIT_COMMITTER_EMAIL='c23@example.com')
if folder.exists():
    for path in folder.rglob('*'):
        if path.is_file():
            os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
    shutil.rmtree(folder)
shutil.copytree(data, folder)
for argv in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'base'], ['update-ref', 'refs/heads/dev', 'HEAD']):
    subprocess.run(['git', '-C', str(folder)] + argv, env=env, check=True)
with open(folder / '.toolchain' / 'project.toml', 'a', encoding='utf-8', newline='') as project:
    project.write(added)
sys.exit(subprocess.run(command).returncode)
