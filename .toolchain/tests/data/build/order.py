# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import sys

log, first, second = sys.argv[1], sys.argv[2], sys.argv[3]
spans = []
for word in (first, second):
    with open('%s.%s' % (log, word), encoding='utf-8') as times:
        spans.append([float(line) for line in times.read().split()])
print('together' if spans[0][0] < spans[1][1] and spans[1][0] < spans[0][1] else 'apart')
