/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include "bridge_schema.h"
#include "bridge_wasm.h"

#define COUNT_FIELDS { uint32_t n; }
BRIDGE_SCHEMA_STRUCT_TYPE(count_t, COUNT_FIELDS);
BRIDGE_SCHEMA_STRUCT_DESC(count_t, COUNT_FIELDS);

static uint32_t count;
static uint32_t counting;

BRIDGE_EXPORT(step) int step(void)
{
    uint32_t table = bridge_get_span_table(bridge_get_span(counting, 0));

    BRIDGE_SET(count_t, n, count, table, 0,
        BRIDGE_GET(count_t, n, count, table, 0) + 1);
    return (0);
}

BRIDGE_EXPORT(init) int init(void)
{
    bridge_term_t terms[1] = {{ 0, BRIDGE_WRITE, BRIDGE_AND, 0 }};
    count_t c = { 0 };

    count = BRIDGE_COMPONENT("test:Count", count_t, BRIDGE_DELETE,
        BRIDGE_TABLE, BRIDGE_ON_DESTROY_REMOVE);
    terms[0].slot = count;
    counting = BRIDGE_ADD_SYSTEM("step", "update", terms, 1, nullptr, 0,
        nullptr, 0);
    BRIDGE_ATTACH(bridge_spawn(), count, c);
    return (0);
}

BRIDGE_EXPORT(reload) int reload(void)
{
    return (1);
}

BRIDGE_EXPORT(shutdown) int shutdown(void)
{
    return (0);
}
