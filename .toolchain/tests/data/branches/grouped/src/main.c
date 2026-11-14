/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

int main(int argc, char **argv)
{
    (void)argv;
    if (argc > 1)
        return (printf("many\n") < 0);
    return (printf("one\n") < 0);
}
