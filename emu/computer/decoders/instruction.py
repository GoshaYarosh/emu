from emu.computer.decoders.decoders import Decoder
#from emu.computer.decoders.shifts import ShiftDecoder


class InstructionDecoder(object):

    @classmethod
    def decode_src_operand(cls, processor, code):
        src_reg_number = Decoder.get_field(code, offset=12, length=4)
        src_value = processor.get_register_value(src_reg_number)
        return src_value

    @classmethod
    def decode_opt_operand(cls, processor, code):
        if Decoder.get_field(code, offset=25, length=1):
            return Decoder.get_field(code, offset=0, length=12)
        else:
            shift = ShiftDecoder.decode(processor, code)
            src_reg_number = Decoder.get_field(code, offset=0, length=4)
            src_value = processor.get_register_value(src_number)
            return shift.perform(src_value)

    operations_names = {
        0b0000: 'and',
        0b0010: 'sub',
        0b0100: 'add',
    }

    @classmethod
    def decode(cls, processor, code):
        operation_type = Decoder.get_field(code, offset=26, length=2)

        if operation_type == 0:
            operation_code = Decoder.get_field(code, offset=21, length=4)
            operation_name = operation_names.get(operation_code, None)
            operation = Operation(operation_name)

            src_value = cls.decode_src_operand(processor, code)
            opt_value = cls.decode_opt_operand(processor, code)
            dst_reg_number = Decoder.get_field(code, offset=12, length=4)
            result = operation.perform(
                processor,
                src_operand,
                opt_operand,
                dst_reg_number
            )

        if Decoder.get_field(code, offset=20, length=1):
            processor.update_flags(result)
