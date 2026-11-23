# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import os
import signal
import sys
import time

NAMES = {0: 'interrupt', 1: 'termination', 2: 'hang-up'}


def say(text):
    # os.write has no buffer, so a handler that writes during another write raises no reentrant error
    os.write(1, (text + os.linesep).encode('ascii'))


def got(name):
    say('got ' + name)
    if name == 'hang-up':
        os._exit(0)


def routine(event):
    if event in NAMES:
        got(NAMES[event])
    return event in NAMES


if os.name == 'nt':
    import ctypes
    ROUTINE = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)(routine)
    ctypes.WinDLL('kernel32').SetConsoleCtrlHandler(ROUTINE, True)
else:
    for number, name in ((signal.SIGINT, 'interrupt'), (signal.SIGTERM, 'termination'), (signal.SIGHUP, 'hang-up')):
        if signal.getsignal(number) != signal.SIG_IGN:
            signal.signal(number, lambda caught, frame, name=name: got(name))
    import select
    wake, woken = os.pipe()
    os.set_blocking(woken, False)
    signal.set_wakeup_fd(woken)
start = time.monotonic()
say('ready')
if os.name != 'nt':
    # a signal just before read() only sets a flag, and read() would block with the handler pending
    while 0 not in select.select([0, wake], [], [])[0]:
        os.read(wake, 64)
sys.stdin.readline()
try:
    if time.monotonic() - start >= 1:
        say('paused')
    say('done')
except OSError:
    os._exit(3)
