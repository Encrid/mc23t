/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "give.h"

char *give(void)
{
    return (malloc(8));
}

void drop(char *block)
{
    free(block);
}
