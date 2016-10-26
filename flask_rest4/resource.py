# coding=utf-8

from .constants import DEFAULT_METHODS, METHOD
from .response import output_json


class Resource(object):
    _extends_ = {}
    _endpoints_ = {}

    def __init__(self):
        extends = self._extends_
        methods = dict(DEFAULT_METHODS, **extends)
        self._endpoints_ = {name: METHOD(methods, name) for name in dir(self)
                            if not name.startswith('_')}
        for name in dir(self):
            if not name.startswith('_'):
                func = output_json(getattr(self, name))
                setattr(self, name, func)


def extend(**extends):
    def add_extends(cls):
        cls._extends_ = extends
        return cls
    return add_extends
