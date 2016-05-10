from emu.handlers.shift import asr
from emu.utils.binary import pretty
from emu.decoders.base import Decoder, ImmediateDecoder
from emu.decoders.shift import ShiftDecoder
from emu.handlers.base import BranchHandler
from emu.handlers.instruction import InstructionHandler
from emu.handlers.condition import ConditionHandler


class InstructionDecoder(Decoder):

    def __init__(self, processor):
        self._processor = processor
        self.str_shifter_operand = ''

    def get_destination_register_number(self, code):
        dest_reg_number = Decoder.get_field(code, offset=12, length=4)
        return dest_reg_number

    def get_source_operand_name(self, code):
        register_number = self.get_field(code, offset=16, length=4)
        register_name = 'r{}'.format(register_number)
        return register_name

    def get_source_operand_value(self, code):
        register_name = self.get_source_operand_name(code)
        return self._processor.registers[register_name]

    def get_shifter_operand_value(self, code):
        is_shift_not_specified = Decoder.get_field(code, offset=25, length=1)
        if is_shift_not_specified:
            immediate = ImmediateDecoder(self._processor).decode(code)
            self.str_shifter_operand = str(immediate)
            return immediate
        else:
            decoder = ShiftDecoder(self._processor)
            self.str_shifter_operand = decoder.to_str(code)
            shift_handler = ShiftDecoder(self._processor).decode(code)
            self.shift_handler = shift_handler
            shifted_value = shift_handler.handle()
            return shifted_value

    def get_condition_handler(self, code):
        condition_code = Decoder.get_field(code, offset=28, length=4)
        return ConditionHandler.get_handler(self._processor, condition_code)

    def to_str(self, code):
        handler = self.decode(code)
        name = handler.get_name()
        if name == 'b':
            offset = Decoder.get_field(code, offset=0, length=24)
            offset = asr(offset << 8, 8) << 2
            offset &= (2 ** 32 - 1)
            offset = offset - 2 ** 32 if offset >> 31 else offset
            return "{}{} {:x}".format(
                name, self.get_condition_handler(code).get_name(),
                offset + 8,
            )

        if name == 'mov':
            return "{}{} {}, {}".format(
                name, self.get_condition_handler(code).get_name(),
                'r{}'.format(self.get_destination_register_number(code)),
                self.str_shifter_operand
            )

        if name in ['tst', 'teq', 'cmp', 'cmn']:
            return "{}{} {}, {}".format(
                name, self.get_condition_handler(code).get_name(),
                self.get_source_operand_name(code),
                self.str_shifter_operand
            )

        else:
            return "{}{} {}, {}, {}".format(
                handler.get_name(), self.get_condition_handler(code).get_name(),
                'r{}'.format(self.get_destination_register_number(code)),
                self.get_source_operand_name(code),
                self.str_shifter_operand
            )


    def decode(self, code):
        instruction_type = Decoder.get_field(code, offset=26, length=2)

        if instruction_type == 0b0:
            dest_reg_number = self.get_destination_register_number(code)
            source_operand = self.get_source_operand_value(code)
            shifter_operand = self.get_shifter_operand_value(code)
            condition_handler = self.get_condition_handler(code)
            instruction_code = Decoder.get_field(code, offset=21, length=4)
            is_state_changing = bool(Decoder.get_field(code, offset=20, length=1))
            return InstructionHandler.get_handler(
                self._processor,
                instruction_code,
                is_state_changing,
                condition_handler,
                source_operand,
                shifter_operand,
                dest_reg_number
            )

        if instruction_type == 0b10:
            offset = Decoder.get_field(code, offset=0, length=24)
            condition = self.get_condition_handler(code)
            return BranchHandler(self._processor, offset, condition)
