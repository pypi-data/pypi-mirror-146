import json
import mmap
import os
import struct

_INITIAL_MMAP_SIZE = 1 << 20
_pack_integer_func = struct.Struct(b'i').pack
_pack_double_func = struct.Struct(b'd').pack
_unpack_integer = struct.Struct(b'i').unpack_from
_unpack_double = struct.Struct(b'd').unpack_from


# struct.pack_into has atomicity issues because it will temporarily write 0 into
# the mmap, resulting in false reads to 0 when experiencing a lot of writes.
# Using direct assignment solves this issue.

def _pack_double(data, pos, value):
    data[pos:pos + 8] = _pack_double_func(value)


def _pack_integer(data, pos, value):
    data[pos:pos + 4] = _pack_integer_func(value)


def _read_all_values(data, used=0):
    """Yield (key, value, pos). No locking is performed."""

    if used <= 0:
        # If not valid `used` value is passed in, read it from the file.
        used = _unpack_integer(data, 0)[0]

    pos = 8

    while pos < used:
        encoded_len = _unpack_integer(data, pos)[0]
        # check we are not reading beyond bounds
        if encoded_len + pos > used:
            raise RuntimeError('Read beyond file size detected, file is corrupted.')
        pos += 4
        encoded_key = data[pos:pos + encoded_len]
        padded_len = encoded_len + (8 - (encoded_len + 4) % 8)
        pos += padded_len
        value = _unpack_double(data, pos)[0]
        yield encoded_key.decode('utf-8'), value, pos
        pos += 8


class MmapedDict:
    """A dict of doubles, backed by an mmapped file.

    The file starts with a 4 byte int, indicating how much of it is used.
    Then 4 bytes of padding.
    There's then a number of entries, consisting of a 4 byte int which is the
    size of the next field, a utf-8 encoded string key, padding to a 8 byte
    alignment, and then a 8 byte float which is the value.

    Not thread safe.
    """

    def __init__(self, filename, read_mode=False):
        self._f = open(filename, 'rb' if read_mode else 'a+b')
        self._fname = filename
        capacity = os.fstat(self._f.fileno()).st_size
        if capacity == 0:
            self._f.truncate(_INITIAL_MMAP_SIZE)
            capacity = _INITIAL_MMAP_SIZE
        self._capacity = capacity
        self._m = mmap.mmap(self._f.fileno(), self._capacity,
                            access=mmap.ACCESS_READ if read_mode else mmap.ACCESS_WRITE)

        self._positions = {}
        self._used = _unpack_integer(self._m, 0)[0]
        if self._used == 0:
            self._used = 8
            _pack_integer(self._m, 0, self._used)
        else:
            if not read_mode:
                for key, _, pos in self._read_all_values():
                    self._positions[key] = pos

    @staticmethod
    def read_all_values_from_file(filename):
        with open(filename, 'rb') as infp:
            # Read the first block of data, including the first 4 bytes which tell us
            # how much of the file (which is preallocated to _INITIAL_MMAP_SIZE bytes) is occupied.
            data = infp.read(mmap.PAGESIZE)
            used = _unpack_integer(data, 0)[0]
            if used > len(data):  # Then read in the rest, if needed.
                data += infp.read(used - len(data))
        return _read_all_values(data, used)

    def _init_value(self, key):
        """Initialize a value. Lock must be held by caller."""
        encoded = key.encode('utf-8')
        # Pad to be 8-byte aligned.
        padded = encoded + (b' ' * (8 - (len(encoded) + 4) % 8))
        value = struct.pack(f'i{len(padded)}sd'.encode(), len(encoded), padded, 0.0)
        while self._used + len(value) > self._capacity:
            self._capacity *= 2
            self._f.truncate(self._capacity)
            self._m = mmap.mmap(self._f.fileno(), self._capacity)
        self._m[self._used:self._used + len(value)] = value

        # Update how much space we've used.
        self._used += len(value)
        _pack_integer(self._m, 0, self._used)
        self._positions[key] = self._used - 8

    def _read_all_values(self):
        """Yield (key, value, pos). No locking is performed."""
        return _read_all_values(data=self._m, used=self._used)

    def read_all_values(self):
        """Yield (key, value). No locking is performed."""
        for k, v, _ in self._read_all_values():
            yield k, v

    def read_value(self, key):
        if key not in self._positions:
            self._init_value(key)
        pos = self._positions[key]
        # We assume that reading from an 8 byte aligned value is atomic
        return _unpack_double(self._m, pos)[0]

    def write_value(self, key, value):
        if key not in self._positions:
            self._init_value(key)
        pos = self._positions[key]
        # We assume that writing to an 8 byte aligned value is atomic
        _pack_double(self._m, pos, value)

    def close(self):
        if self._f:
            self._m.close()
            self._m = None
            self._f.close()
            self._f = None


def mmap_key(metric_name, name, labelnames, labelvalues):
    """Format a key for use in the mmap file."""
    # ensure labels are in consistent order for identity
    labels = dict(zip(labelnames, labelvalues))
    return json.dumps([metric_name, name, labels], sort_keys=True)
