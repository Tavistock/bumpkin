from bumpkin.models.string import BString


class BSymbol(BString):
    """
    B Symbol. Basically a String.
    """

    def __init__(self, string):
        self += string
