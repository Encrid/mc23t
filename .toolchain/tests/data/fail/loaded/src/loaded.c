/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>

#include "loaded.h"

static int said(const char *text, int status)
{
    puts(text);
    return (status);
}

int main(void)
{
    if (pid_loaded() < 0)
        return (said("no id", 1));
    return (said("one id through a pointer", 0));
}
