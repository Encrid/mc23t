/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "heap.h"

[[clang::export_name("pick")]] int pick(int x)
{
    int *kept = malloc(sizeof(*kept));
    int picked;

    if (!kept)
        return (-1);
    *kept = x;
    picked = *kept > 0 ? 1 : 0;
    free(kept);
    return (picked);
}
