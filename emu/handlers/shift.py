def asr(value, shift_amount):
    for shift_step in xrange(shift_amount):
        high_bit = value & (1 << 31)
        value = (value >> 1) | high_bit
    return value


def ror(value, shift_amount):
    for shift_step in xrange(shift_amount):
        low_bit = (value & 1) << 31
        value = (value >> 1) | low_bit
    return value


def lsl(value, shift_amount):
    int32_mask = (1 << 32) - 1
    return (value << shift_amount) & int32_mask


def lsr(value, shift_amount):
    return value >> shift_amount


class Shift(object):

    def __init__(self, shift_code, shift_name, callback):
        self.code = shift_code
        self.name = shift_name
        self.callback = callback


class ShiftHandler(object):

    shifts = {
        0b00: Shift(0b00, 'lsl', lsl),
        0b01: Shift(0b01, 'lsr', lsr),
        0b10: Shift(0b10, 'asr', asr),
        0b11: Shift(0b11, 'ror', ror),
    }

    @classmethod
    def get_handler(cls, shift_code, shifted_value, shift_amount):
        try:
            shift_handler = ShiftHandler(cls.shifts[shift_code])
            shift_handler.set_operands(shifted_value, shift_amount)
            return shift_handler
        except KeyError as e:
            raise ValueError('Unknown shift code: {}'.format(shift_code))

    def __init__(self, shift):
        self._shift = shift

    def get_shift_name(self):
        return self._shift.name

    def get_shift_code(self):
        return self._shift.code

    def set_operands(self, value, shift_amount):
        if not 0 <= value <= 2 ** 32 - 1:
            raise ValueErorr('Value must be 32-bit integer number')
        self._value = value
        self._shift_amount = shift_amount

    def handle(self):
        return self._shift.callback(self._value, self._shift_amount)
