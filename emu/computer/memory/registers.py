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

    def __init__(self, count, initial_value=0):
        self._registers = {
            'r{}'.format(index): Register(0)
            for index in xrange(count)
        }
        self._registers.update({
            'sp': Register(0),
            'pc': Register(0)
        })

    def __getitem__(self, reg_name):
        return self._registers[reg_name].get_value()

    def __setitem__(self, reg_name, value):
        if reg_name in ['sp']:
            raise KeyError('Register SP cannot be modified directly')
        return self._registers[reg_name].set_value(value)

    def count(self):
        return len(self._registers)
