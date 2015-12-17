#from processor.decoders.decoders import Decoder
#from processor.operations.shifts import Shift

class ShiftDecoder(Decoder):

    shift_names = {
        0b00: 'asr',
        0b01: 'lsl',
        0b10: 'rsl',
        0b11: 'ror',
    }

    # @classmethod
    # def decode(cls, processor, instruction_code):
    #     if Decoder.get_code(instruction_code, offset=4, length=1):
    #         reg_number = Decoder.get_code(instruction_code, offset=8, length=4)
    #         positions = processor.get_register_value(reg_number)
    #     else:
    #         positions = Decoder.get_code(instruction_code, offset=7, length=5)
    #
    #     shift_code = Decoder.get_code(instruction_code, offset=5, length=2)
    #     return Shift(shift_names[shift_code], positions)
