from processor.operations.operations import Operation


class Shift(Operation):

    @staticmethod
    def arithmetic_right_shift(value, positions):
        return value

    @staticmethod
    def rotate_right_shift(value, positions):
        return value

    @staticmethod
    def logical_left_shift(value, positions):
        return (value << positions) & (1 << 32 - 1)

    @staticmethod
    def logical_right_shift(value, positions):
        return value >> positions;

    @staticmethod
    def carry_right_shift(value, carry):
        return value >> 1 | (carry << 31)

    shifts = {
        'ars': Shift.arithmetic_right_shift,
        'lsl': Shift.logical_left_shift,
        'lsr': Shift.logical_right_shift,
        'ror': Shift.rotate_right_shift,
        'rrx': Shift.carry_right_shift,
    }

    def __init__(self, name, positions):
        self._name = name
        self._positions = positions
        self._handler = self.shifts[name]

    def perform(self, value):
        return self._hanler(value, self._positions)
