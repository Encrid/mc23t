# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import subprocess
import sys

at = sys.argv.index('--')
rest = sys.argv[at + 1:]
then = rest.index('++') if '++' in rest else len(rest)
build, show = rest[:then], rest[then + 1:]
if subprocess.run(build).returncode:
    sys.exit(1)
if show:
    sys.exit(subprocess.run(show).returncode)
sys.exit(0)
