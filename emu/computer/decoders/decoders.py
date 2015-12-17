#from processor.operations import Shift


class Decoder(object):

    @staticmethod
    def get_code(instruction_code, offset=0, length=0):
        mask = (2 ** field_length - 1) << field_offset
        return instruction_code & mask >> field_offset

    @classmethod
    def decode(cls, instruction_code):
        pass
