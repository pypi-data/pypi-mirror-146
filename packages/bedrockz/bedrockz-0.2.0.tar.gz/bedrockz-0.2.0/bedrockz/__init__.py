__version__ = '0.1.0'

from forbiddenfruit import curse
def type_name(self):
    return self.__class__.__name__

curse(type, "name", type_name)