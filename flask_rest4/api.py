# coding=utf-8

from .utils import inject_url_rule, auto_complete_rule
from .resource import output_json


class Api(object):
    def __init__(self, app_or_blueprint):
        self.app = app_or_blueprint
        self.routes = []

    def route(self, rule, methods):
        def decorator(func):
            self.register_api(rule, methods, func)
            return func
        return decorator

    def register_api(self, rule, methods, func):
        func = output_json(func)
        endpoint = func.__name__
        rule = auto_complete_rule(rule)
        inject_url_rule(self.app, rule, methods, endpoint, func)
        route = (rule, methods, func)
        self.routes.append(route)
