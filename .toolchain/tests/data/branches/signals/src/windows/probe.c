/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <string.h>

#include "probe.h"

int probe_write(const char *mode)
{
    if (!strcmp(mode, "open"))
        return (0);
    if (!strcmp(mode, "pending"))
        return (-1);
    return (12);
}
