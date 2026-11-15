/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "take.h"

bool take_one(void)
{
    char *one = malloc(8);
    bool taken = one != nullptr;

    free(one);
    return (taken);
}

bool take_two(void)
{
    char *one = malloc(8);
    char *two = one ? malloc(8) : nullptr;
    bool taken = two != nullptr;

    free(two);
    free(one);
    return (taken);
}
