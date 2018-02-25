'''Rest4 api

Main apis for Rest4
'''


import inspect
import re

from flask import abort, request

from . import response, settings, errors


class Api(object):
    def __init__(self, app_or_blueprint):
        self.app = app_or_blueprint
        self.routes = []
        self.rule_resources = {}

    def route(self, rule, *methods, add_default_option=True):
        def decorator(resource_or_func):
            if inspect.isclass(resource_or_func) and \
               issubclass(resource_or_func, Resource):
                self.register_resource(resource_or_func, rule)
            else:
                default_api_methods = settings.DEFAULT_API_METHODS
                self.register_api(rule,
                                  methods or default_api_methods,
                                  resource_or_func,
                                  add_default_option)
            return resource_or_func
        return decorator

    def register_api(self, rule, methods, func, add_default_option=True):
        if add_default_option:
            option_methods = settings.DEFUALT_OPTION_METHODS
            option_api = CommonApi(rule, option_methods, default_option)
            option_route = (option_api.rule, option_api.methods, option_api)
            whatever(lambda: self.inject_route(option_route))
        common_api = CommonApi(rule, methods, func)
        route = (common_api.rule, common_api.methods, common_api)
        return self.inject_route(route)

    def register_resource(self, resource, rule):
        if rule in self.rule_resources:
            raise errors.ConflictResourceRule(rule)
        res = resource(rule)
        self.rule_resources[res.rule] = res
        batch_rule, item_rule = analyze_rule(rule)
        routes = sorted(((batch_rule if e.batch else item_rule, e.methods, e)
                         for e in res.endpoints if not e.extra),
                        key=lambda x: x[:1])
        return self.inject_routes(routes)

    def inject_routes(self, routes):
        return [self.inject_route(route) for route in routes]

    def inject_route(self, route):
        rule, methods, endpoint_or_func = route
        endpoint = "{}-{}".format(rule, endpoint_or_func.name)
        self.app.add_url_rule(rule,
                              endpoint=endpoint,
                              view_func=endpoint_or_func,
                              methods=methods)
        self.routes.append(route)
        return route

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
    '''Resource class
    Example book:
    rule: /book/<book_id>

    options    ->    /book             OPTION
    list       ->    /book             GET
    create     ->    /book             POST
    extras     ->    /book             PUT

    option     ->    /book/<book_id>   OPTION
    get        ->    /book/<book_id>   GET
    update     ->    /book/<book_id>   PUT
    patch      ->    /book/<book_id>   PATCH
    delete     ->    /book/<book_id>   DELETE
    extra      ->    /book/<book_id>   POST
    '''
    _extra_map = {}
    _extras_map = {}
    _excludes = ["name"]

    def __init__(self, rule):
        self.name = type(self).__name__
        self.endpoints = [self._endpoint(e) for e in self._real_endpoints()]
        self.rule = rule

    def extras(self, *args, **kwargs):
        return self._extras_endpoint(*args, **kwargs)

    def extra(self, *args, **kwargs):
        return self._extra_endpoint(*args, **kwargs)

    def options(self, *args, **kwargs):
        return default_option(*args, **kwargs)

    def option(self, *args, **kwargs):
        return default_option(*args, **kwargs)

    def _endpoint(self, endpoint):
        endpoint = Endpoint(self, endpoint)
        if endpoint.extra:
            extra_map = self._extras_map if endpoint.batch else self._extra_map
            extra_map[endpoint.func_name] = endpoint
        return endpoint

    def _extras_endpoint(self, *args, **kwargs):
        endpoint_name = request.json.get(settings.ENDPOINT_KEY_NAME)
        endpoint = self._extras_map.get(endpoint_name)
        return endpoint(*args, **kwargs) if endpoint else abort(404)

    def _extra_endpoint(self, *args, **kwargs):
        endpoint_name = request.json.get(settings.ENDPOINT_KEY_NAME)
        endpoint = self._extra_map.get(endpoint_name)
        return endpoint(*args, **kwargs) if endpoint else abort(404)

    def _real_endpoints(self):
        return (getattr(self, name) for name in dir(self)
                if not name.startswith('_') and name not in self._excludes)

    def __repr__(self):
        return "<Resource {}>".format(self.name)

    def __str__(self):
        return "<Resource {}>".format(self.name)


class Endpoint(object):
    def __init__(self, resource, func):
        self.resource = resource
        self.func_name = func.__name__
        self.alias = getattr(func, 'alias', self.func_name)
        self.name = "{}.{}".format(self.resource.name, self.func_name)
        self.batch = self._is_batch(func)
        self.methods, self.extra = self._get_methods_and_extra()
        self.func = func if self.extra else response.output_json(func)

    def _is_batch(self, func):
        keywords = settings.BATCH_FUNCTION_KEYWORDS
        return getattr(func, 'batch', None) or \
            any(keyword in self.alias for keyword in keywords)

    def _get_methods_and_extra(self):
        methods_map = settings.FUNCTION_METHODS_MAP
        default = methods_map['extras'] if self.batch else methods_map['extra']
        method = methods_map.get(self.alias)
        return (method or default,), not method

    def __call__(self, *arg, **kwargs):
        return self.func(*arg, **kwargs)

    def __repr__(self):
        return "<Endpoint {}>".format(self.name)

    def __str__(self):
        return "<Endpoint {}>".format(self.name)


class CommonApi(object):
    def __init__(self, rule, methods, func):
        self.func_name = func.__name__
        self.name = self.func_name
        self.methods = methods
        self.func = response.output_json(func)
        self.rule = rule

    def __call__(self, *arg, **kwargs):
        return self.func(*arg, **kwargs)

    def __repr__(self):
        return "<CommonApi {}>".format(self.name)

    def __str__(self):
        return "<CommonApi {}>".format(self.name)


def alias(alias_name):
    def decorator(func):
        func.alias = alias_name
        return func
    return decorator


def batch(func):
    func.batch = True
    return func


def auto_complete_rule(rule):
    return rule if rule.endswith('/') else rule + '/'


def analyze_rule(rule):
    rule = auto_complete_rule(rule)

    match = re.match(r'^(.*)<\w+?>/$', rule)
    if not match:
        raise errors.InvalidError(rule)

    batch_rule = match.groups()[0]
    item_rule = rule
    return batch_rule, item_rule


def rule_add_suffix(rule, suffix):
    return auto_complete_rule(rule + suffix)


def default_option(*args, **kwargs):
    return settings.DEFAULT_OPTION_RESPONSE_DATA


def whatever(func):
    try:
        return func()
    except:
        pass
