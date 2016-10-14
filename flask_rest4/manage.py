# coding=utf-8


def list_RESTful_apis(*rules):
    for rule in rules:
        list_RESTful_apis_for_rule(rule)


def list_RESTful_apis_for_rule(rule):
    for resource, routes in rule.routes.items():
            print(resource)
            for route in routes:
                print(route)
