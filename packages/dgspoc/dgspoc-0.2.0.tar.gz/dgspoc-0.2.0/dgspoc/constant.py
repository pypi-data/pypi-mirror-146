
from enum import IntFlag


class FrameworkValue:
    def __init__(self, value):
        self.value = str(value)

    def __eq__(self, other):
        value1 = self.value.lower()
        if isinstance(other, self.__class__):
            value2 = other.value.lower()
        else:
            value2 = str(other).lower()

        chk_lst = ['rf', 'robotframework']
        value1, value2 = value1.replace(' ', ''), value2.replace(' ', '')

        if value1 in chk_lst and value2 in chk_lst:
            return True
        else:
            result = value1 == value2
            return result

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return self.value


class ECODE(IntFlag):
    SUCCESS = 0
    BAD = 1


class FWTYPE:
    UNITTEST = FrameworkValue('unittest')
    PYTEST = FrameworkValue('pytest')
    ROBOTFRAMEWORK = FrameworkValue('robotframework')
