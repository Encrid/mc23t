/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "rows.h"
#include "word.h"

static int twice(const char *word)
{
    char *twice = word_twice(word);

    printf("%s\n", twice ? twice : "no memory");
    free(twice);
    return (twice ? 0 : 1);
}

static int run(int count, char **words)
{
    const char *mode = count > 1 ? words[1] : "";
    const char *shown = getenv("WORD");

    if (!strcmp(mode, "twice") && count > 2)
        return (twice(words[2]));
    if (!strcmp(mode, "show"))
        return (printf("%s\n", shown ? shown : "no WORD"), 0);
    if (!strcmp(mode, "say")) {
        for (int i = 2; i < count; i++)
            printf("[%s]", words[i]);
        return (printf(" from %s\n", words[0]), 0);
    }
    return (printf("no mode '%s'\n", mode), count);
}

int main(void)
{
    return (rows_run(run));
}
