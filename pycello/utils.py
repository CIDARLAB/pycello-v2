__author__ = 'Timothy S. Jones <jonests@bu.edu>, Densmore Lab, BU'
__license__ = 'GPL3'


def find_by_name(name, objects):
    """Find a TargetData object by name.

    Parameters
    ----------
    name : str
    objects : collections.abc.Iterable

    """
    for o in objects:
        if o.name == name:
            return o
