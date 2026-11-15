/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdlib.h>
#include <string.h>

#include "word.h"

char *word_twice(const char *word)
{
    size_t len = strlen(word);
    char *twice = malloc(2 * len + 1);

    if (!twice)
        return (nullptr);
    memcpy(twice, word, len);
    memcpy(twice + len, word, len + 1);
    return (twice);
}
