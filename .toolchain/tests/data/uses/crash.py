# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import os
import subprocess
import sys

tools, folder, how = sys.argv[1], sys.argv[2], sys.argv[3]
holder = subprocess.Popen([sys.executable, os.path.join(tools, 'locks.py'), folder, '60', 'gpu'],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
holder.stdout.readline()
if how == 'kill':
    holder.kill()
    holder.wait()
os.environ['MC23T_LOCKS'] = folder
sys.path.insert(0, tools)
import locks

handle = locks.opened('gpu')
print('free' if locks.took(handle) else 'taken')
holder.kill()
holder.wait()
