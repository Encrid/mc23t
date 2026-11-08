/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "probe.h"

static void dump_hits(void)
{
    const char *path = getenv("C23_BRANCHES");
    FILE *file = path ? fopen(path, "rb") : nullptr;
    unsigned char bytes[64];
    size_t got = 0;

    if (!file)
        return;
    got = fread(bytes, 1, sizeof(bytes), file);
    fclose(file);
    printf("hits");
    for (size_t i = 0; i < got; i++)
        printf(" %02x", bytes[i]);
    printf("\n");
}

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "closed";
    const char *form = argc > 2 ? argv[2] : "write";

    if (!strcmp(form, "variant"))
        printf("%s %s %d
", mode, form, probe_variant(mode));
    else if (!strcmp(form, "hoisted"))
        printf("%s %s %d
", mode, form, probe_hoisted(mode));
    else
        printf("%s %s %d
", mode, form, probe_write(mode));
    dump_hits();
    return (0);
}
