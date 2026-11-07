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

    printf("%s wrote %d\n", mode, probe_write(mode));
    return (0);
}
