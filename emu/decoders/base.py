from emu.handlers.shift import ror


class Decoder(object):

    @staticmethod
    def get_field(instruction_code, offset=0, length=0):
        mask = (2 ** length - 1) << offset
        return (instruction_code & mask) >> offset


class ImmediateDecoder(object):

    def __init__(self, processor):
        self._processor = processor

    def decode(cls, code):
        immediate = Decoder.get_field(code, offset=0, length=8)
        rotate = Decoder.get_field(code, offset=8, length=4)
        return ror(immediate, 2 * rotate)
