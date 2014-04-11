from bumpkin.models import BObject


class BString(BObject, unicode):
    """
    Generic Hy String object. Helpful to store string literals from Hy
    scripts. It's either a ``str`` or a ``unicode``, depending on the
    Python version.
    """
    pass
