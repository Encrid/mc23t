/*
** Copyright (C) 2026 Enkrid
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
#include <stdio.h>
#include <stdlib.h>

#if defined(__x86_64__)
[[gnu::target("fma")]]
#endif
static double add_product(double a, double b, double c)
{
    return (a * b + c);
}

int main(int argc, char **argv)
{
    volatile double product;
    double a;
    double b;
    double c;

    if (argc != 4)
        return (2);
    a = strtod(argv[1], nullptr);
    b = strtod(argv[2], nullptr);
    c = strtod(argv[3], nullptr);
    product = a * b;
    puts(add_product(a, b, c) == product + c ? "separate" : "fused");
    return (0);
}
