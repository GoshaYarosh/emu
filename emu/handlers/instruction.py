def invert(value):
    return value ^ (2 ** 32 - 1)


def is_negative(value):
    return bool((value & (2 ** 32 - 1)) >> 31)


def is_zero(value):
    return not (value & (2 ** 32 - 1))


def is_carried(value):
    return not 0 <= value <= 2 ** 32 - 1


def is_overflowed(value, a, b):
    if is_negative(a) == is_negative(b):
        return is_negative(value) != is_negative(a)
    else:
        return False


class Instruction(object):

    def __init__(self, code, name, callback):
        self.code = code
        self.name = name
        self.callback = callback


class InstructionHandler(object):

    instructions = {
        0b0000: Instruction(0b0000, 'and', lambda a, b, c: a & b),
        0b0001: Instruction(0b0001, 'eor', lambda a, b, c: a ^ b),
        0b0010: Instruction(0b0010, 'sub', lambda a, b, c: a - b),
        0b0011: Instruction(0b0011, 'rsb', lambda a, b, c: b - a),
        0b0100: Instruction(0b0100, 'add', lambda a, b, c: a + b),
        0b0101: Instruction(0b0101, 'adc', lambda a, b, c: a + b + inverse(c)),
        0b0110: Instruction(0b0110, 'sbc', lambda a, b, c: a - b - inverse(c)),
        0b0111: Instruction(0b0111, 'rsc', lambda a, b, c: b - a - inverse(c)),
        0b1000: Instruction(0b1000, 'tst', lambda a, b, c: a & b),
        0b1001: Instruction(0b1001, 'teq', lambda a, b, c: a ^ b),
        0b1010: Instruction(0b1010, 'cmp', lambda a, b, c: a - b),
        0b1011: Instruction(0b1011, 'cmn', lambda a, b, c: a + b),
        0b1100: Instruction(0b1100, 'orr', lambda a, b, c: a | b),
        0b1101: Instruction(0b1101, 'mov', lambda a, b, c: b),
        0b1110: Instruction(0b1110, 'bic', lambda a, b, c: a & invert(b)),
        0b1111: Instruction(0b1111, 'mvn', lambda a, b, c: invert(a)),
    }

    @classmethod
    def get_handler(cls, processor, code, is_state_changing, condition_handler,
                    source_value, shifter_value, dst_reg_number):
        try:
            handler = InstructionHandler(processor, cls.instructions[code])
            handler.set_operands(is_state_changing, source_value, condition_handler,
                                 shifter_value, dst_reg_number)
            return handler
        except KeyError as e:
            raise ValueError('Unknown instruction code {}'.format(code))

    def __init__(self, processor, instruction):
        self._processor = processor
        self._instruction = instruction

    def get_name(self):
        return self._instruction.name

    def get_code(self):
        return self._instruction.code

    def get_dst_reg_name(self):
        return 'r{}'.format(self._dst_reg_number)

    def set_operands(self, is_state_changing, source_value, condition_handler,
                     shifter_value, dst_reg_number):
        self._source_value = source_value
        self._shifter_value = shifter_value
        self._dst_reg_number = dst_reg_number
        self._is_state_changing = is_state_changing
        self._condition_handler = condition_handler

    def handle(self):
        if self._condition_handler.handle():
            result_value = self._instruction.callback(self._source_value, self._shifter_value, 0)
            register_name = 'r{}'.format(self._dst_reg_number)
            if self._is_state_changing:
                self._processor.state.update_flag('z', is_zero(result_value))
                self._processor.state.update_flag('n', is_negative(result_value))
                self._processor.state.update_flag('c', is_carried(result_value))
                self._processor.state.update_flag('v', is_overflowed(result_value, self._source_value, self._shifter_value))

            if self.get_name() not in ['tst', 'teq', 'cmp', 'cmn']:
                self._processor.registers[register_name] = result_value & (2 ** 32 - 1)
