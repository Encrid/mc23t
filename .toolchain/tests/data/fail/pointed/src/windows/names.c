/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include "pointed.h"

int name_known(void)
{
    return (GetProcAddress(GetModuleHandleW(NULL), "take_value") != nullptr);
}
