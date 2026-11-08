/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <string.h>

#include "probe.h"

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "closed";
    const char *form = argc > 2 ? argv[2] : "write";

    if (!strcmp(form, "variant"))
        printf("%s %s %d\n", mode, form, probe_variant(mode));
    else if (!strcmp(form, "hoisted"))
        printf("%s %s %d\n", mode, form, probe_hoisted(mode));
    else
        printf("%s %s %d\n", mode, form, probe_write(mode));
    return (0);
}
