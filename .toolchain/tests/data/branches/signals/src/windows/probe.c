/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <string.h>

#include "probe.h"

int probe_write(const char *mode)
{
    return (!strcmp(mode, "open") ? 0 : -1);
}

int probe_variant(const char *mode)
{
    (void)mode;
    return (0);
}

int probe_hoisted(const char *mode)
{
    (void)mode;
    return (0);
}
