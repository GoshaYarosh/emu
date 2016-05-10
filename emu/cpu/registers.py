from collections import OrderedDict


class Register(object):

    def __init__(self, initial_value=0):
        self.set_value(initial_value)

    def set_value(self, value):
        if not abs(value) < 2 ** 32 - 1:
            raise ValueError('Value must be 32-bit int number')
        self._value = value

    def get_value(self):
        return self._value


class RegistersManager(object):

    def __init__(self, registers_count, initial_value=0):
        self._registers = OrderedDict((
            ('sp',  Register(initial_value)),
            ('pc', Register(initial_value))
        ))
        self._registers.update(
            ('r{}'.format(index), Register(initial_value))
            for index in xrange(registers_count)
        )

    def count(self):
        return len(self._registers)

    def __iter__(self):
        return self._registers.iteritems()

    def __getitem__(self, register_name):
        return self._registers[register_name].get_value()

    def __setitem__(self, register_name, value):
        return self._registers[register_name].set_value(value)
