/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

static bool is_ready(int value)
{
    void *kept = malloc(1);

    free(kept);
    return (value > 0);
}

int main(int argc, char **argv)
{
    int wrote = argc > 1 ? atoi(argv[1]) : 0;
    int failed = argc > 2 ? atoi(argv[2]) : 1;
    int before = argc > 3 ? atoi(argv[3]) : 0;

    if (wrote && failed == 1 && !before) {
        if (is_ready(wrote) == true)
            printf("waited\n");
    }
    printf("done\n");
    return (0);
}
