/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "pointed.h"

int main(void)
{
    int value = take_value(21);

    if (value < 0) {
        printf("no value\n");
        return (1);
    }
    printf("value %d\n", value);
    return (0);
}
