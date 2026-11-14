# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import subprocess
import sys
from pathlib import Path

at = sys.argv.index('--')
then = sys.argv.index('++') if '++' in sys.argv else len(sys.argv)
changed, text = sys.argv[1], sys.argv[2]
build, show = sys.argv[at + 1:then], sys.argv[then + 1:]
if subprocess.run(build).returncode:
    sys.exit(1)
if changed == '-':
    sys.exit('the second build changes no input')
after = text.replace('|N|', chr(10)).encode('utf-8')
if Path(changed).read_bytes() == after:
    sys.exit('the second build reads the same input')
Path(changed).write_bytes(after)
if subprocess.run(build).returncode:
    sys.exit(1)
sys.exit(subprocess.run(show).returncode)
