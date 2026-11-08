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
    int number = 0;
    int ends[2] = {-1, -1};
    int wrote = 0;

    if (pipe(ends))
        return (-3);
    if (strcmp(mode, "open"))
        close(ends[0]);
    sigemptyset(&pipe_only);
    sigaddset(&pipe_only, SIGPIPE);
    pthread_sigmask(SIG_BLOCK, &pipe_only, &old);
    errno = 0;
    wrote = write(ends[1], "x", 1);
    wrote = wrote < 0 ? -1 : 0;
    if (wrote && errno == EPIPE) {
        if (pipe_waiting() == true)
            sigwait(&pipe_only, &number);
    }
    pthread_sigmask(SIG_SETMASK, &old, nullptr);
    close(ends[0]);
    close(ends[1]);
    return (wrote);
}

int probe_variant(const char *mode)
{
    sigset_t pipe_only;
    sigset_t old;
    int number = 0;
    int ends[2] = {-1, -1};

    if (pipe(ends))
        return (-3);
    close(ends[0]);
    sigemptyset(&pipe_only);
    sigaddset(&pipe_only, SIGPIPE);
    pthread_sigmask(SIG_BLOCK, &pipe_only, &old);
    if (!strcmp(mode, "ignore"))
        signal(SIGPIPE, SIG_IGN);
    errno = 0;
    if (write(ends[1], "x", 1) < 0 && errno == EPIPE) {
        if (pipe_waiting() == true)
            sigwait(&pipe_only, &number);
        if (!strcmp(mode, "ignore") && pipe_waiting() == true)
            number = 2;
    }
    pthread_sigmask(SIG_SETMASK, &old, nullptr);
    close(ends[0]);
    close(ends[1]);
    return (number);
}

int probe_hoisted(const char *mode)
{
    sigset_t pipe_only;
    sigset_t old;
    bool waiting = false;
    int number = 0;
    int ends[2] = {-1, -1};

    if (pipe(ends))
        return (-3);
    close(ends[0]);
    sigemptyset(&pipe_only);
    sigaddset(&pipe_only, SIGPIPE);
    pthread_sigmask(SIG_BLOCK, &pipe_only, &old);
    if (!strcmp(mode, "ignore"))
        signal(SIGPIPE, SIG_IGN);
    errno = 0;
    if (write(ends[1], "x", 1) < 0 && errno == EPIPE) {
        waiting = pipe_waiting();
        if (waiting == true)
            sigwait(&pipe_only, &number);
    }
    pthread_sigmask(SIG_SETMASK, &old, nullptr);
    close(ends[0]);
    close(ends[1]);
    return (number);
}
