/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <string.h>

#include "things.h"

int main(int argc, char **argv)
{
    void *thing = open_thing(8);

    if (argc < 2 || strcmp(argv[1], "kept"))
        close_thing(thing);
    printf("done\n");
    return (0);
}
