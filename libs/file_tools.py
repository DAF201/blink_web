from hashlib import sha256
from pickle import dumps, loads
from io import BytesIO
from math import sqrt, ceil


def data_slice(data, chunk_size):
    if type(data) != bytes:
        data = dumps(data)
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def data_hash(chunks):
    return [sha256(x) for x in chunks]


def virtual_file(data):
    if type(data) != bytes:
        data = dumps(data)
    return BytesIO(data)


def data_dimension_rounding(data_size):
    size = ceil(sqrt(data_size))
    if size**2 - data_size < 4:
        size += 1
    return size
