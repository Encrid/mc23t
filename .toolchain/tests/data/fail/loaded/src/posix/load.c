/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <dlfcn.h>
#include <sys/types.h>
#include <unistd.h>

#include "loaded.h"

int pid_loaded(void)
{
    pid_t (*run)(void) = (pid_t (*)(void))dlsym(RTLD_DEFAULT, "getpid");

    if (!run)
        return (-1);
    return (run() < 1 ? -1 : 0);
}
