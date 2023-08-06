
import re

from jmespath import functions


class CustomFunctions(functions.Functions):

    @functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_re_search(self, s, pattern):
        return re.search(pattern, s) is not None


