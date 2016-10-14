# coding=utf-8

from .api import ApiRule
from .rule import Rule
from .resource import Resource  # noqa


class RESTful(object):
    def __init__(self, app):
        self.app = app

    def bind_to(self, app_or_blueprint):
        rule = Rule(app_or_blueprint)
        return rule


class Api(object):
    def __init__(self, app):
        self.app = app

    def bind_to(self, app_or_blueprint):
        api = ApiRule(app_or_blueprint)
        return api
