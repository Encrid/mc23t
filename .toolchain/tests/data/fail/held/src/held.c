/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "held.h"

void mine(void)
{
    if (wait_turn())
        puts("main refused");
    puts("main");
    fflush(stdout);
    done();
}

int main(void)
{
    if (both())
        return (puts("no thread"), 1);
    return (0);
}
