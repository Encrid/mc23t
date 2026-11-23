/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <string.h>

#include "outcomes.h"

int main(int argc, char **argv)
{
    static unsigned char ones[4096];
    size_t start = argc > 2 ? strtoull(argv[1], nullptr, 10) : 0;
    size_t count = argc > 2 ? strtoull(argv[2], nullptr, 10) : 0;

    if (count > sizeof(ones))
        return (2);
    memset(ones, 1, sizeof(ones));
    printf("%s\n", c23_outcomes_keep(ones, start, count) ? "kept" : "refused");
    return (0);
}
