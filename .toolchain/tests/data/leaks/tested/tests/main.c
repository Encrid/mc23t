/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "give.h"
#include "modes.h"

static char *kept;

static void run_two(void)
{
    char *own = malloc(8);
    char *first = give();
    char *second = give();

    printf("%s %s\n", first ? "made" : "none", second ? "made" : "none");
    free(own);
    drop(first);
    drop(second);
}

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "";
    char said[16];

    if (!strcmp(mode, MODE_FREES))
        free(give());
    if (!strcmp(mode, MODE_GIVES))
        drop(malloc(8));
    if (!strcmp(mode, MODE_KEEPS))
        kept = malloc(8);
    if (!strcmp(mode, MODE_TWO))
        run_two();
    sprintf(said, "%.15s", mode);
    printf("%s\n", said);
    return (kept == nullptr && !strcmp(mode, MODE_KEEPS));
}
