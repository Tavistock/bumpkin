from bumpkin.models import BObject


class BInteger(BObject, long):
    """
    Internal represntation of a B Integer. May raise a ValueError as if
    int(foo) was called, given HyInteger(foo). On python 2.x long will
    be used instead
    """

    def __new__(cls, number, *args, **kwargs):
        number = long(number)
        return super(BInteger, cls).__new__(cls, number)
