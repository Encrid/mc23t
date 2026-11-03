/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

#define TWICE(a) ((a) * 2)
#define SAME(b) b
#define PICK(c) c ? 0 : 1
#define BOTH(d) d && d
#define IFPOS(e) if ((e) > 0)

int main(int argc, char **argv)
{
    int x = argc > 1 ? atoi(argv[1]) : 0;
    int y = argc > 2 ? atoi(argv[2]) : 0;

    if (TWICE(x) == 4)
        puts("twice");
    if (SAME(x) == SAME(y))
        puts("same");
    if (x == TWICE(y))
        puts("double");
    if (SAME(x) && y)
        puts("and");
    if (x == PICK(y) + 1)
        puts("pick");
    if (BOTH(x))
        puts("both");
    IFPOS(y)
        puts("positive");
    return (0);
}
