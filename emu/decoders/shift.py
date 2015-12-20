from emu.handlers.shift import ShiftHandler
from emu.decoders.base import Decoder
from emu.utils.binary import pretty

class ShiftDecoder(object):

    def __init__(self, processor):
        self._processor = processor

    def get_shifter_name(self, code):
        register_number = Decoder.get_field(code, offset=0, length=4)
        register_name = 'r{}'.format(register_number)
        return register_name

    def get_shifted_value(self, code):
        register_name = self.get_shifter_name(code)
        value = self._processor.registers[register_name]
        return value

    def get_shift_amount(self, code):
        is_amount_in_register = Decoder.get_field(code, offset=4, length=1)
        if is_amount_in_register:
            register_number = Decoder.get_field(code, offset=8, length=4)
            register_name = 'r{}'.format(register_number)
            shift_value = self._processor.registers[register_name]
            self.shift_amount_str = register_name 
        else:
            shift_value = Decoder.get_field(code, offset=7, length=5)
            self.shift_amount_str = str(shift_value) if shift_value != 0 else None
        return shift_value

    def decode(self, code):
        shift_code = Decoder.get_field(code, offset=5, length=2)
        shifted_value = self.get_shifted_value(code)
        shift_amount = self.get_shift_amount(code)
        return ShiftHandler.get_handler(
            shift_code, shifted_value, shift_amount
        )

    def to_str(self, code):
        handler = self.decode(code)
        if self.shift_amount_str:
            return "{}, {} {}".format(
                self.get_shifter_name(code), 
                handler.get_name(), 
                self.shift_amount_str
            )
        else:
            return "{}".format(self.get_shifter_name(code))
