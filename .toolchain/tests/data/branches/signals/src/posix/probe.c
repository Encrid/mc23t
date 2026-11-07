/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <errno.h>
#include <signal.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

#include "probe.h"

static bool pipe_waiting(void)
{
    sigset_t waiting;

    sigemptyset(&waiting);
    sigpending(&waiting);
    return (sigismember(&waiting, SIGPIPE) == 1);
}

int probe_write(const char *mode)
{
    sigset_t pipe_only;
    sigset_t old;
    bool before = false;
    int number = 0;
    int ends[2] = {-1, -1};
    int wrote = 0;

    if (!strcmp(mode, "ignore") && signal(SIGPIPE, SIG_IGN) == SIG_ERR)
        return (-2);
    if (pipe(ends))
        return (-3);
    if (strcmp(mode, "open"))
        close(ends[0]);
    sigemptyset(&pipe_only);
    sigaddset(&pipe_only, SIGPIPE);
    pthread_sigmask(SIG_BLOCK, &pipe_only, &old);
    if (!strcmp(mode, "pending"))
        raise(SIGPIPE);
    errno = 0;
    before = pipe_waiting();
    wrote = write(ends[1], "x", 1);
    if (wrote < 0)
        wrote = -1;
    if (wrote && errno == EPIPE && !before) {
        if (pipe_waiting() == true)
            sigwait(&pipe_only, &number);
    }
    pthread_sigmask(SIG_SETMASK, &old, nullptr);
    close(ends[0]);
    close(ends[1]);
    return (wrote);
}
