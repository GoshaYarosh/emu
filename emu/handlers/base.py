from emu.handlers.shift import asr


class Handler(object):

    def __init__(self, code, name, function):
        self._code = code
        self._name = name
        self._function = function


    def handle(self):
        pass


class BranchHandler(object):

    def __init__(self, processor, offset):
        self._processor = processor
        self._offset = offset

    def get_name(self):
        return 'b'

    def get_code(self):
        return 0

    def handle(self):
        offset = self._offset
        offset = asr(self._offset << 8, 8) << 2
        offset &= (2 ** 32 - 1)
        offset = offset - 2 ** 32 if offset >> 31 else offset
        print self._processor.registers['pc'], offset + 4
        self._processor.registers['pc'] += offset + 4
