# coding=utf-8


def list_restful_apis(*rules):
    for rule in rules:
        list_restful_apis_for_rule(rule)


def list_restful_apis_for_rule(rule):
    for resource, routes in rule.routes.items():
            print(resource)
            for route in routes:
                print(route)
