from bumpkin.models.list import BList


class BExpression(BList):
    """
    B S-Expression. Basically just a list.
    """

    def __repr__(self):
        return "(%s)" % (" ".join([repr(x) for x in self]))
