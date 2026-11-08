# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import sys

data = open(sys.argv[1], "rb").read()
sys.stdout.write("found %s\n" % (b"one" in data or b"two" in data))
