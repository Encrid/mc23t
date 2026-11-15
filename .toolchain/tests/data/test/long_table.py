# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import subprocess
import sys
from pathlib import Path

ROW = '    { name = "long %d", in = "%s", claims = { has = ["%s"] }, false = "none" },\n'
TABLE = '''[[case]]
name = "long"
run = ["{python}", "-c", "import sys\\nfor line in sys.stdin:\\n    print(line.strip() * 10)\\n    print()"]
claims = { status = 0 }
rows = [
%s]
'''


def main():
    case, tool, word = sys.argv[1:]
    rows = ''.join(ROW % (at, 'a' * 2000, word) for at in range(60))
    folder = Path(case) / 'tests' / 'cases'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'long.toml').write_text(TABLE % rows, encoding='utf-8', newline='\n')
    sys.exit(subprocess.run([sys.executable, tool, '--root', case, '--out', case + '/out']).returncode)


if __name__ == '__main__':
    main()
