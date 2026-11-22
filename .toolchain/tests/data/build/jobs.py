# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import sys

sys.path.insert(0, sys.argv[1])
import shared

print(shared.jobs_of({}, int(sys.argv[2])))
