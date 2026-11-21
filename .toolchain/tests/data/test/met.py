# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import sys
import time
from pathlib import Path

folder, me, other, seconds, mode = Path(sys.argv[1]), sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
folder.mkdir(parents=True, exist_ok=True)
(folder / me).touch()
end = time.monotonic() + seconds
seen = False
while not seen and time.monotonic() < end:
    seen = (folder / other).exists()
    time.sleep(0.05)
if mode == 'apart':
    (folder / me).unlink()
sys.exit(0 if seen == (mode == 'meet') else 1)
