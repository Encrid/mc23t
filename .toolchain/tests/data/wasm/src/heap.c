/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "heap.h"

void *malloc(size_t size)
{
    static unsigned char heap[256];
    static size_t used;

    if (size > sizeof(heap) - used)
        return (nullptr);
    used += size;
    return (heap + used - size);
}

void free([[maybe_unused]] void *at)
{
}
