# coding=utf-8


def list_restful_apis(*restful_apis):
    for restful_api in restful_apis:
        list_restful_api(restful_api)


def list_restful_api(restful_api):
    for resource, routes in restful_api.routes.items():
        print(resource)
        for rule, methods, func in routes:
            print(route_string(rule, methods, func))


def list_common_apis(apis):
    for rule, methods, func in apis.routes:
        print(route_string(rule, methods, func))


def route_string(rule, methods, func):
    return "{} {} {}".format(rule, methods, func.__name__)
