

__all__ = ['JmesPathContainerMixin', 'JpDict', 'JpList']


from functools import partial

import jmespath
from salix_jmespath_tools import CustomFunctions


_options = jmespath.Options(custom_functions=CustomFunctions())
_jpr = partial(jmespath.search, options=_options)


class JmesPathContainerMixin():

    def jp(self, expr):
        return _jpr(expr, self)


class JpDict(JmesPathContainerMixin, dict):
    pass


class JpList(JmesPathContainerMixin, dict):
    pass
