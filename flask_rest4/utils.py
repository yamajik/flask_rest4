# coding=utf-8


def classfy_dict(data, func):
    match = {}
    not_match = {}

    for key, value in data.items():
        if func(key, value):
            match[key] = value
        else:
            not_match[key] = value

    return match, not_match


def inject_url_rule(app_or_blueprint, rule, func, methods):
    methods = methods.split()
    app_or_blueprint.add_url_rule(rule, view_func=func, methods=methods)
