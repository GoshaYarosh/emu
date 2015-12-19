class Condition(object):

    def __init__(self, code, name, callback):
        self.code = code
        self.name = name
        self.callback = callback

class ConditionHandler(object):

    conditions = {
        0b0000: Condition(0b0000, 'eq', lambda c, z, n, v: z),
        0b0001: Condition(0b0001, 'ne', lambda c, z, n, v: not z),
        0b0010: Condition(0b0010, 'cs', lambda c, z, n, v: c),
        0b0011: Condition(0b0011, 'cc', lambda c, z, n, v: not c),
        0b0100: Condition(0b0100, 'mi', lambda c, z, n, v: n),
        0b0101: Condition(0b0101, 'pl', lambda c, z, n, v: not n),
        0b0110: Condition(0b0110, 'vs', lambda c, z, n, v: v),
        0b0111: Condition(0b0111, 'vs', lambda c, z, n, v: not v),
        0b1000: Condition(0b1000, 'hi', lambda c, z, n, v: c and not z),
        0b1001: Condition(0b1001, 'ls', lambda c, z, n, v: not c or z),
        0b1010: Condition(0b1010, 'ge', lambda c, z, n, v: n == v),
        0b1011: Condition(0b1011, 'lt', lambda c, z, n, v: n != v),
        0b1100: Condition(0b1100, 'gt', lambda c, z, n, v: n == v and not z),
        0b1101: Condition(0b1101, 'le', lambda c, z, n, v: n != v or not z),
        0b1110: Condition(0b1110, 'al', lambda c, z, n, v: True),
        0b1111: Condition(0b1111, '', lambda c, z, n, v: True),
    }

    @classmethod
    def get_handler(cls, processor, code):
        try:
            handler = ConditionHandler(processor, cls.conditions[code])
            return handler
        except KeyError as e:
            raise ValueError('Unknown instruction code {}'.format(code))

    def __init__(self, processor, condition):
        self._processor = processor
        self._condition = condition

    def get_name(self):
        return self._condition.name

    def get_code(self):
        return self._condition.code

    def handle(self):
        is_carried = self._processor.state.get_flag('c')
        is_zero = self._processor.state.get_flag('z')
        is_negative = self._processor.state.get_flag('n')
        is_overflowed = self._processor.state.get_flag('v')
        return self._condition.callback(
            is_carried, is_zero,
            is_negative, is_overflowed
        )
