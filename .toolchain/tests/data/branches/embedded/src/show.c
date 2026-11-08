/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

static const char WORD[] = {
#embed "word.txt"
};

int main(int argc, char **argv)
{
    if (argc > 1)
        printf("%s\n", argv[1]);
    else
        printf("%.*s", (int)sizeof(WORD), WORD);
    return (0);
}
