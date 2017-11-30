# coding=utf-8

import inspect
import itertools
import re

from collections import OrderedDict
from .response import output_json, default_option


BATCH_SIGNS = ['batch', 'list', 'create', 'options']
METHODS = {
    'options': 'OPTION',
    'list': 'GET',
    'create': 'POST',
    'option': 'OPTION',
    'get': 'GET',
    'update': 'PUT',
    'patch': 'PATCH',
    'delete': 'DELETE'
}
PRIORITIES = {
    'options': 1,
    'list': 2,
    'create': 3,
    'option': 101,
    'get': 102,
    'update': 103,
    'patch': 104,
    'delete': 105
}


def get_methods(name):
    return (METHODS.get(name, 'POST'), )


def get_suffix(name):
    return "" if name in METHODS else name


def is_batch(name):
    return any(sign in name for sign in BATCH_SIGNS)


def get_priority(name):
    return PRIORITIES.get(name)


class Api(object):
    def __init__(self, app_or_blueprint):
        self.app = app_or_blueprint
        self.routes = []
        self.rule_resources = {}

    def route(self, rule, *methods):
        def decorator(resource_or_func):
            if inspect.isclass(resource_or_func) and \
               issubclass(resource_or_func, Resource):
                self.register_resource(resource_or_func, rule)
            else:
                self.register_api(rule, methods or ("POST",), resource_or_func)
            return resource_or_func
        return decorator

    def register_api(self, rule, methods, func):
        func = output_json(func)
        route = (rule, methods, func)
        self.inject_routes(route)

    def register_resource(self, resource, rule):
        if rule in self.rule_resources:
            raise Exception('Already have rule : "{}"'.format(rule))
        res = resource()
        self.rule_resources[rule] = res
        routes = self.generate_routes(rule, res)
        self.inject_routes(*routes)

    def generate_routes(self, rule, resource):
        resource.rules.append(rule)
        route_tuple = lambda e: (self._add_suffix(rule, e), e.methods, e)
        routes = (route_tuple(e) for e in resource.endpoints)
        return sorted(routes, key=lambda x: x[-1].priority)

    def inject_routes(self, *routes):
        routes_dict = OrderedDict()
        for route in routes:
            rule, methods, _ = route
            routes_dict.setdefault(rule, {"methods": set(), "routes": []})
            routes_dict[rule]["methods"].update(methods)
            routes_dict[rule]["routes"].append(route)
        for rule, item in routes_dict.items():
            if 'OPTION' not in item["methods"]:
                methods = ('OPTION',)
                route = (rule, methods, default_option)
                self.inject_route(route)
            for route in item["routes"]:
                self.inject_route(route)

    def inject_route(self, route):
        self.routes.append(route)
        rule, methods, endpoint_or_func = route
        endpoint = "{}-{}".format(rule, endpoint_or_func.name)
        self.app.add_url_rule(rule,
                              endpoint=endpoint,
                              view_func=endpoint_or_func,
                              methods=methods)

    def _add_suffix(self, rule, endpoint):
        batch_rule, item_rule = analyze_rule(rule)
        rule_str = batch_rule if endpoint.batch else item_rule
        return rule_add_suffix(rule_str, endpoint.suffix)

    def __str__(self):
        routes_str = ""
        for rule, methods, endpoint_or_func in self.routes:
            routes_str += "\n  {:<40} {:<20} {:<20} ".format(
                rule, ', '.join(methods), endpoint_or_func.name)
        return "<Rest4 Api of {}: {}\n>".format(self.app.name, routes_str)

    def __repr__(self):
        routes_str = ""
        for rule, methods, endpoint_or_func in self.routes:
            routes_str += "\n  {:<40} {:<20} {:<20} ".format(
                rule, ', '.join(methods), endpoint_or_func.name)
        return "<Rest4 Api of {}: {}\n>".format(self.app.name, routes_str)



class Resource(object):
    rules = []
    excludes = ["name", "endpoints", "endpoint",
                "excludes", "rules", "get_priority"]

    def __init__(self):
        self._max_batch_endpoint_priority = 2
        self._max_item_endpoint_priority = 104

        self.name = type(self).__name__
        self.endpoints = [Endpoint(self, e) for e in self._real_endpoints()]

    def endpoint(self, name):
        if name not in self.endpoints:
            raise Exception("No such endpoint '{}' in {}".format(name, self))
        return self.endpoints[name]

    def get_priority(self, name, batch):
        return PRIORITIES.get(name) or self._next_priority(batch)

    def _next_priority(self, batch):
        return self._next_batch_priority() if batch \
            else self._next_item_priority()

    def _next_item_priority(self):
        self._max_item_endpoint_priority += 1
        return self._max_item_endpoint_priority

    def _next_batch_priority(self):
        self._max_batch_endpoint_priority += 1
        return self._max_batch_endpoint_priority

    def _real_endpoints(self):
        return (getattr(self, name) for name in dir(self)
                if not name.startswith('_') and name not in self.excludes)

    def __repr__(self):
        return "<Resource {}>".format(self.name)

    def __str__(self):
        return "<Resource {}>".format(self.name)


class Endpoint(object):
    def __init__(self, resource, func):
        self.resource = resource
        self.func = output_json(func)
        self.func_name = func.__name__
        self.name = "{}.{}".format(self.resource.name, self.func_name)
        self.methods = getattr(func, 'methods', get_methods(self.func_name))
        self.suffix = getattr(func, 'suffix', get_suffix(self.func_name))
        self.batch = getattr(func, 'batch', is_batch(self.func_name))
        self.priority = self.resource.get_priority(self.func_name, self.batch)

    def __call__(self, *arg, **kargs):
        return self.func(*arg, **kargs)

    def __repr__(self):
        return "<Endpoint {}>".format(self.name)

    def __str__(self):
        return "<Endpoint {}>".format(self.name)


def auto_complete_rule(rule):
    return rule if rule.endswith('/') else rule + '/'


def analyze_rule(rule):
    rule = auto_complete_rule(rule)

    match = re.match(r'^(.*)<\w+?>/$', rule)
    if not match:
        raise Exception

    batch_rule = match.groups()[0]
    item_rule = rule
    return batch_rule, item_rule


def rule_add_suffix(rule, suffix):
    return auto_complete_rule(rule + suffix)
