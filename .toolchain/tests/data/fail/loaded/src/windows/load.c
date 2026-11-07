/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include "loaded.h"

int pid_loaded(void)
{
    DWORD (*run)(void) = (DWORD (*)(void))GetProcAddress(
        GetModuleHandleW(L"kernel32.dll"), "GetCurrentProcessId");

    if (!run)
        return (-1);
    return (run() == 0 ? -1 : 0);
}
