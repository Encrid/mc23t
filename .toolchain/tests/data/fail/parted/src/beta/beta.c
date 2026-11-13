/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char *block = malloc(8);

    if (!block)
        return (printf("no memory\n") < 0);
    free(block);
    return (printf("made\n") < 0);
}
