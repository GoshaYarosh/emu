class RandomAccessMemory(object):

    def __init__(self, memory_size, initial_value=0):
        if not 0 <= initial_value <= 256:
            raise ValueError('Default value must be in range [0..256]')
        self._array = bytearray([initial_value] * memory_size)

    def __len__(self):
        return len(self._array)

    def __iter__(self):
        return self._array.__iter__()

    def __getitem__(self, address):
        if isinstance(address, slice):
            if len(self) <= address.stop:
                raise IndexError('address is out of memory size')
            return self._array[address.start:address.stop:address.step]
        else:
            if len(self) <= address:
                raise IndexError('address is out of memory size')
            return self._array[address]

    def __setitem__(self, address, value):
        if not 0 <= value <= 256:
            raise ValueError('Default value must be in range [0..256]')
        if (len(self) <= address):
            raise IndexError('address is out of memory size')
        self._array[address] = value


class RandomAccessMemoryManager(object):

    def __init__(self, memory_size, initial_value=0):
        self._memory = RandomAccessMemory(memory_size, initial_value)
        self._image_len = memory_size

    def __iter__(self):
        return self._memory.__iter__()

    def size(self):
        return len(self._memory)

    def read_bytes(self, start_address, bytes_count):
        return self._memory[start_address:start_address + bytes_count]

    def read_byte(self, address):
        return self._memory[address]

    def write_byte(self, address, value):
        self._memory[address] = value

    def get_image_len(self):
        return self._image_len

    def load_image(self, binary_image):
        if (len(binary_image) > len(self._memory)):
            raise IndexError('Size of the image must be less than memory size')
        self._image_len = len(binary_image)
        for address in xrange(len(binary_image)):
            self._memory[address] = binary_image[address]
