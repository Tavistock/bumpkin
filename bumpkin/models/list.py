from bumpkin.models import BObject


class BList(BObject, list):
    """
    B List. Basically just a list.
    """

    def replace(self, other):
        for x in self:
            x.replace(other)

        BObject.replace(self, other)
        return self

    def __add__(self, other):
        return self.__class__(super(BList, self).__add__(other))

    def __getslice__(self, start, end):
        return self.__class__(super(BList, self).__getslice__(start, end))

    def __getitem__(self, item):
        ret = super(BList, self).__getitem__(item)

        if isinstance(item, slice):
            return self.__class__(ret)

        return ret

    def __repr__(self):
        return "[%s]" % (" ".join([repr(x) for x in self]))
