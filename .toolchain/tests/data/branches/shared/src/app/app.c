/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "core/core.h"

int main(int argc, char **argv)
{
    (void)argv;
    if (argc > 1)
        printf("app many\n");
    else
        printf("app one\n");
    printf("pick %d\n", core_pick(1));
    return (0);
}
