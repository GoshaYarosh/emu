class Operation(object):

    operations = {
        'and': lambda o1, o2: o1 & o2,
        'add': lambda o1, o2: o1 + o2,
        'sub': lambda o1, r2: o1 - o2,
    }

    def __init__(self, name):
        self._name = name
        self._code = code

    def perform(self, processor, src_value, opt_value, dst_reg_number):
        return src_value
