/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

static const char WORD[] = {
#embed "word.txt"
    , 0
};

int main(void)
{
    printf("%s", WORD);
    return (0);
}
