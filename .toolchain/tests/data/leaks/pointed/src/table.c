/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>

#include "things.h"

static void *made(int size)
{
    return (malloc((size_t)size));
}

static void freed(void *thing)
{
    free(thing);
}

open_thing_t open_thing = made;
close_thing_t close_thing = freed;
