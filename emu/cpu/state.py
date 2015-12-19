class StateManager(object):

    def __init__(self):
        self._flags = {
            'n': False,
            'z': False,
            'c': False,
            'v': False,
        }

    def get_flag(self, flag_name):
        try:
            return self._flags[flag_name]
        except KeyError as e:
            raise ValueError('Unknown flag name: {}'.format(flag_name))

    def update_flag(self, flag_name, value):
        try:
            self._flags[flag_name] = value
        except KeyError as e:
            raise ValueError('Unknown flag name: {}'.format(flag_name))

    def set_flag(self, flag_name):
        try:
            self._flags[flag_name] = True
        except KeyError as e:
            raise ValueError('Unknown flag name: {}'.format(flag_name))

    def clear_flag(self, flag_name):
        try:
            self._flags[flag_name] = False
        except KeyError as e:
            raise ValueError('Unknown flag name: {}'.format(flag_name))
