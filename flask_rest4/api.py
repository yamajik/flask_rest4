# coding=utf-8

from .utils import inject_url_rule
from .resource import output_json


class ApiRule(object):
    def __init__(self, app_or_blueprint):
        self.app = app_or_blueprint
        self.routes = {}

    def route(self, rule, methods):
        def decorator(func):
            func = output_json(func)
            return self.register_api(rule, func, methods)
        return decorator

    def register_api(self, rule, func, methods):
        inject_url_rule(self.app, rule, func, methods)
