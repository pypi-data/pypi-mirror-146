
__all__ = ['jp', 'CustomFunctions']


from functools import partial

import jmespath

from .customfunctions import CustomFunctions


# Define the jp convenience function
_options = jmespath.Options(custom_functions=CustomFunctions())
jp = partial(jmespath.search, options=_options)

