/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#ifndef THINGS_H
    #define THINGS_H

typedef void *(*open_thing_t)(int size);
typedef void (*close_thing_t)(void *thing);

extern open_thing_t open_thing;
extern close_thing_t close_thing;

#endif
