/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#ifndef SHARED_CORE_H
    #define SHARED_CORE_H

static inline int core_sign(int value)
{
    if (value < 0)
        return (-1);
    return (1);
}

int core_pick(int value);

#endif
