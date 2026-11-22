/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <windows.h>

#include "held.h"

static DWORD WINAPI run(LPVOID arg)
{
    worker();
    return (arg != nullptr);
}

int both(void)
{
    HANDLE thread = CreateThread(nullptr, 0, run, nullptr, 0, nullptr);

    if (!thread)
        return (-1);
    mine();
    WaitForSingleObject(thread, INFINITE);
    CloseHandle(thread);
    return (0);
}
