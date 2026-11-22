/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "held.h"

void worker(void)
{
    if (wait_turn())
        puts("worker refused");
    puts("worker");
    fflush(stdout);
    done();
}
