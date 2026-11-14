/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "core/core.h"

int core_pick(int value)
{
    int *box = malloc(sizeof(int));
    int kept = 0;

    if (box == nullptr)
        return (-1);
    *box = value > 10 ? 10 : value;
    kept = *box;
    free(box);
    return (kept);
}
