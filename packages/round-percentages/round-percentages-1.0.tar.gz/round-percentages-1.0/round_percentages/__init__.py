import sys

from .round_percentages import round_percentages as rp


# Masquerade the module as a function by using a callable class
class round_percentages:
    def __call__(self, *args, **kwargs):
        return rp(*args, **kwargs)


sys.modules[__name__] = round_percentages()
