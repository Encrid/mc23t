# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import sys

sys.path.insert(0, sys.argv[1])
import fetch
import shared

nowhere = sys.argv[4:] == ['nowhere']
sys.argv[1:] = ['--root', sys.argv[2], '--out', sys.argv[3]]
args = shared.arguments()
config = shared.config(args.root)
folders = []
for target in shared.built_by(config, shared.this_target(config['targets'])):
    values = shared.variables(config, args, target, 'zig')
    if nowhere:
        values['home'] = ''
    fetch.sources(config, values, True)
    folders.append(values['sample'])
print('%d targets, %d folders' % (len(folders), len(set(folders))))
