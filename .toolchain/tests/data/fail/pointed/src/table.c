/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "pointed.h"

static int doubled(int base)
{
    return (base * 2);
}

take_value_t take_value = doubled;
