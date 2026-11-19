# Copyright (C) 2026 Enkrid
#
# Under the GNU Affero General Public License, version 3 only: see license.
import ctypes
import struct
from pathlib import Path


class Vector(ctypes.Structure):
    _fields_ = [('size', ctypes.c_size_t), ('data', ctypes.c_void_p)]


class Value(ctypes.Structure):
    _fields_ = [('kind', ctypes.c_uint8), ('of', ctypes.c_int64)]


def loaded(folder):
    found = sorted(path for path in Path(folder).glob('*wasmtime*') if path.suffix in ('.dll', '.so', '.dylib'))
    if not found:
        raise SystemExit('host.py: %s holds no wasmtime' % folder)
    lib = ctypes.CDLL(str(found[0]))
    for name in ('wasm_engine_new', 'wasm_store_new', 'wasm_module_new', 'wasm_instance_new', 'wasm_extern_as_func',
                 'wasm_extern_as_memory', 'wasm_extern_as_global', 'wasm_memory_data', 'wasm_func_call'):
        getattr(lib, name).restype = ctypes.c_void_p
    lib.wasm_memory_data_size.restype = ctypes.c_size_t
    for name in ('wasm_store_new', 'wasm_extern_as_func', 'wasm_extern_as_memory', 'wasm_extern_as_global',
                 'wasm_memory_data', 'wasm_memory_data_size', 'wasm_exporttype_name'):
        getattr(lib, name).argtypes = [ctypes.c_void_p]
    lib.wasm_exporttype_name.restype = ctypes.POINTER(Vector)
    return lib


def instance(lib, data):
    store = lib.wasm_store_new(lib.wasm_engine_new())
    binary = ctypes.create_string_buffer(data, len(data))
    module = lib.wasm_module_new(ctypes.c_void_p(store), ctypes.byref(Vector(len(data), ctypes.addressof(binary))))
    if not module:
        raise SystemExit('host.py: wasmtime refuses the module')
    made = lib.wasm_instance_new(ctypes.c_void_p(store), ctypes.c_void_p(module), ctypes.byref(Vector(0, None)), None)
    if not made:
        raise SystemExit('host.py: the module does not start')
    types, externs = Vector(), Vector()
    lib.wasm_module_exports(ctypes.c_void_p(module), ctypes.byref(types))
    lib.wasm_instance_exports(ctypes.c_void_p(made), ctypes.byref(externs))
    names = (ctypes.c_void_p * types.size).from_address(types.data)
    items = (ctypes.c_void_p * externs.size).from_address(externs.data)
    named = {}
    for at in range(types.size):
        name = lib.wasm_exporttype_name(names[at]).contents
        named[ctypes.string_at(name.data, name.size).decode()] = items[at]
    return named


def memory(lib, named):
    held = lib.wasm_extern_as_memory(named['memory'])
    return (ctypes.c_ubyte * lib.wasm_memory_data_size(held)).from_address(lib.wasm_memory_data(held))


def area(lib, named, bytes_):
    value = Value()
    lib.wasm_global_get(ctypes.c_void_p(lib.wasm_extern_as_global(named['c23b_outcomes'])), ctypes.byref(value))
    at = value.of & 0xffffffff
    return struct.unpack_from('<7I', bytes(bytes_[at:at + 28]))


def called(lib, named, name, number):
    func = lib.wasm_extern_as_func(named[name])
    given, got = Value(0, number), Value()
    trap = lib.wasm_func_call(ctypes.c_void_p(func), ctypes.byref(Vector(1, ctypes.addressof(given))),
                              ctypes.byref(Vector(1, ctypes.addressof(got))))
    if trap:
        raise SystemExit('host.py: %s(%d) traps' % (name, number))
    return ctypes.c_int32(got.of).value


def run(folder, module, failed, part):
    lib = loaded(folder)
    named = instance(lib, Path(module).read_bytes())
    bytes_ = memory(lib, named)
    version, _, _, _, _, plan, room = area(lib, named, bytes_)
    text = failed.encode() + b'\0' + part.encode() + b'\0'
    if version != 1 or len(text) > room:
        raise SystemExit('host.py: the module has no room for the plan')
    bytes_[plan:plan + len(text)] = text
    print('pick: ' + ' '.join(str(called(lib, named, 'pick', n)) for n in (1, 2, 3)))
    print('plan:' + bytes(bytes_[plan:plan + len(text)]).split(b'\0')[0].decode())
