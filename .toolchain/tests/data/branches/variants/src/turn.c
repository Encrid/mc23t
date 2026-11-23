/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    int value = argc > 1 ? atoi(argv[1]) : 0;

#ifdef TURNED
    if (value > 1)
        value = -value;
#endif
    printf("%d\n", value);
    return (0);
}
