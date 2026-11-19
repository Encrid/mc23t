import struct
import sys
from pathlib import Path


def number(data, at):
    value, shift = 0, 0
    while True:
        byte = data[at]
        at += 1
        value |= (byte & 0x7f) << shift
        shift += 7
        if byte < 0x80:
            return value, at


def sections(data):
    found, at = {}, 8
    while at < len(data):
        size, start = number(data, at + 1)
        found.setdefault(data[at], []).append(data[start:start + size])
        at = start + size
    return found


def items(body):
    count, at = number(body, 0)
    return count, at


def exports(body):
    count, at = items(body)
    found = {}
    for _ in range(count):
        size, at = number(body, at)
        name = body[at:at + size].decode()
        kind, index = body[at + size], number(body, at + size + 1)
        found[name], at = (kind, index[0]), index[1]
    return found


def constant(body, at):
    code, at = body[at], at + 1
    if code in (0x41, 0x42, 0x23):
        value, at = number(body, at)
    else:
        value, at = None, at + {0x43: 4, 0x44: 8}[code]
    if body[at] != 0x0b:
        raise SystemExit('a global or a segment has an expression of more than 1 instruction')
    return (value if code == 0x41 else None), at + 1


def globals(body, imported):
    count, at = items(body)
    found = []
    for _ in range(count):
        value, at = constant(body, at + 2)
        found.append(value)
    return [None] * imported + found


def imported_globals(body):
    count, at, globals_found = *items(body), 0
    for _ in range(count):
        for _ in range(2):
            size, at = number(body, at)
            at += size
        kind = body[at]
        at += 1
        if kind == 0x03:
            globals_found += 1
            at += 2
        elif kind == 0x02:
            limits = body[at]
            at = number(body, number(body, at + 1)[1])[1] if limits & 1 else number(body, at + 1)[1]
        elif kind == 0x01:
            limits = body[at + 1]
            at = number(body, number(body, at + 2)[1])[1] if limits & 1 else number(body, at + 2)[1]
        else:
            at = number(body, at)[1]
    return globals_found


def memory(body):
    count, at = items(body)
    image = bytearray()
    for _ in range(count):
        flags, at = number(body, at)
        if flags == 2:
            index, at = number(body, at)
        else:
            index = 0
        start, at = constant(body, at) if flags in (0, 2) else (None, at)
        size, at = number(body, at)
        if index == 0 and start is not None:
            image.extend(bytes(max(0, start + size - len(image))))
            image[start:start + size] = body[at:at + size]
        at += size
    return image


def word(image, at):
    return struct.unpack('<I', bytes(image[at:at + 4]).ljust(4, b'\0'))[0]


def chunks(image, at, end, counts):
    while at < end:
        first = word(image, at)
        if not first:
            at += 4
            continue
        second = word(image, at + 4)
        if counts:
            path = image[at + 8 + 8 * first:at + 8 + 8 * first + second].decode()
            print('counts: %s with %d slots' % (path, first))
            at += (8 + 8 * first + second + 1 + 7) // 8 * 8
        else:
            print('outcomes: %d bytes at %d' % (first, second))
            at += (8 + first + 3) // 4 * 4


def shown(data):
    found = sections(data)
    named = exports(found.get(7, [b'\0'])[0])
    print('exports: ' + ' '.join(sorted(named)))
    if 'c23b_outcomes' not in named:
        return
    values = globals(found[6][0], imported_globals(found[2][0]) if 2 in found else 0)
    image = memory(found.get(11, [b'\0'])[0])
    area = values[named['c23b_outcomes'][1]]
    version, outcomes, outcomes_end, counts, counts_end, _, room = (word(image, area + 4 * n) for n in range(7))
    print('area: version %d, room %d' % (version, room))
    chunks(image, outcomes, outcomes_end, False)
    chunks(image, counts, counts_end, True)


if __name__ == '__main__':
    shown(Path(sys.argv[1]).read_bytes())
