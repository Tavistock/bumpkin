

class BObject(object):
    """
    Generic B Object model. This is helpful to inject things into all the
    B lexing Objects at once.
    """

    def replace(self, other):
        if isinstance(other, BObject):
            for attr in ["start_line", "end_line",
                         "start_column", "end_column"]:
                if not hasattr(self, attr) and hasattr(other, attr):
                    setattr(self, attr, getattr(other, attr))
        else:
            raise TypeError("Can't replace a non B object with a B object")

        return self
