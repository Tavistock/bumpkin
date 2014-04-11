from bumpkin.models import BObject


class BFloat(BObject, float):
    """
    B Float
    """

    def __new__(cls, number, *args, **kwargs):
        number = float(number)
        return super(BFloat, cls).__new__(cls, number)
