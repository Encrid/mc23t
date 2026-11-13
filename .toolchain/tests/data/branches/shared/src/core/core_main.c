/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "core/core.h"

int main(void)
{
    printf("core %d\n", core_pick(1));
    printf("core %d\n", core_pick(20));
    printf("sign %d %d\n", core_sign(-1), core_sign(1));
    return (0);
}
