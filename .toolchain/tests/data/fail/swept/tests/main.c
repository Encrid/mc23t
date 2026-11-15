/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <string.h>

#include "sweep.h"
#include "take.h"

int main(int count, char **words)
{
    bool one = count > 1 && !strcmp(words[1], "one");
    bool taken = false;
    unsigned at = 0;

    do {
        at++;
        sweep_refuse("malloc", at);
        taken = one ? take_one() : take_two();
        if (sweep_is_refused())
            printf("malloc %u refused: %s\n", at, taken ? "taken" : "nothing taken");
    } while (sweep_is_refused());
    printf("%u refused calls, then %s\n", at - 1, taken ? "taken" : "nothing taken");
    return (0);
}
