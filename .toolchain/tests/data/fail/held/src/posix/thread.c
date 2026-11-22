/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <pthread.h>

#include "held.h"

static void *run(void *arg)
{
    worker();
    return (arg);
}

int both(void)
{
    pthread_t thread;

    if (pthread_create(&thread, nullptr, run, nullptr))
        return (-1);
    mine();
    pthread_join(thread, nullptr);
    return (0);
}
