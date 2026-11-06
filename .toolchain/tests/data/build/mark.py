# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import shutil
import sys
import time

log, word, seconds = sys.argv[1], sys.argv[2], float(sys.argv[3])
start = time.time()
with open(log, 'a', encoding='utf-8') as out:
    out.write('start %s\n' % word)
time.sleep(seconds)
with open(log, 'a', encoding='utf-8') as out:
    out.write('end %s\n' % word)
with open('%s.%s' % (log, word), 'w', encoding='utf-8') as times:
    times.write('%f\n%f\n' % (start, time.time()))
if len(sys.argv) >= 6:
    shutil.copyfile(sys.argv[4], sys.argv[5])
