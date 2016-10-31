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


def inject_url_rule(app_or_blueprint, rule, methods, endpoint, func):
    methods = methods.split()
    app_or_blueprint.add_url_rule(rule, endpoint=endpoint,
                                  view_func=func, methods=methods)


def auto_complete_rule(rule):
    if not rule.endswith('/'):
        return rule + '/'
    else:
        return rule
