from bumpkin.models import BObject


class BComplex(BObject, complex):
    """
    B Complex
    """

    def __new__(cls, number, *args, **kwargs):
        number = complex(number)
        return super(BComplex, cls).__new__(cls, number)
