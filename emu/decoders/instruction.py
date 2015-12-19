from emu.utils.binary import pretty
from emu.decoders.base import Decoder, ImmediateDecoder
from emu.decoders.shift import ShiftDecoder
from emu.handlers.base import BranchHandler
from emu.handlers.instruction import InstructionHandler
from emu.handlers.condition import ConditionHandler

class InstructionDecoder(Decoder):

    def __init__(self, processor):
        self._processor = processor

    def get_destination_register_number(self, code):
        dest_reg_number = Decoder.get_field(code, offset=12, length=4)
        return dest_reg_number

    def get_source_operand_value(self, code):
        register_number = self.get_field(code, offset=16, length=4)
        register_name = 'r{}'.format(register_number)
        return self._processor.registers[register_name]

    def get_shifter_operand_value(self, code):
        is_shift_not_specified = Decoder.get_field(code, offset=25, length=1)
        if is_shift_not_specified:
            immediate = ImmediateDecoder(self._processor).decode(code)
            return immediate
        else:
            shift_handler = ShiftDecoder(self._processor).decode(code)
            shifted_value = shift_handler.handle()
            return shifted_value

    def get_condition_handler(self, code):
        condition_code = Decoder.get_field(code, offset=28, length=4)
        return ConditionHandler.get_handler(self._processor, condition_code)

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
            return BranchHandler(self._processor, offset)
