# coding=utf-8

import re

from .constants import DEFAULT_ENDPOINTS
from .utils import classfy_dict, inject_url_rule


class Rule(object):
    def __init__(self, app_or_blueprint):
        self.app = app_or_blueprint
        self.routes = {}

    def route(self, rule):
        def decorator(Resource):
            return self.register_resource(rule, Resource)
        return decorator

    def register_resource(self, rule, Resource):
        batch_rule, item_rule = _analyze_rule(rule)

        def register_resource(Resource):
            resource = Resource()
            resource_name = type(resource).__name__

            def is_batch_endpoint(func_name, methods):
                batch_signs = ['batch', 'list', 'create']
                return any(sign in func_name for sign in batch_signs)

            batch_endpoints, item_endpoints = classfy_dict(
                resource._endpoints_, is_batch_endpoint)

            def reject_rule(func_name, methods, is_batch):
                rule = batch_rule if is_batch else item_rule
                if func_name not in DEFAULT_ENDPOINTS:
                    rule += (func_name + '/')
                func = getattr(resource, func_name)
                inject_url_rule(self.app, rule, func, methods)
                return rule, methods, func_name

            batch_routes = [reject_rule(func_name, methods, True)
                            for func_name, methods in batch_endpoints.items()]
            item_routes = [reject_rule(func_name, methods, False)
                           for func_name, methods in item_endpoints.items()]
            self.routes[resource_name] = batch_routes + item_routes

        return register_resource(Resource)


def _analyze_rule(rule):
    if not rule.endswith('/'):
        rule += '/'

    match = re.match(r'^(.*)<\w+?>/$', rule)
    if not match:
        raise Exception

    batch_rule = match.groups()[0]
    item_rule = rule
    return batch_rule, item_rule
