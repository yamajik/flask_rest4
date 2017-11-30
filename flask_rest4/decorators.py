# coding=utf-8


def suffix(name):
    def decorator(func):
        func.suffix = name
        return func
    return decorator

def methods(*http_methods):
    def decorator(func):
        func.methods = http_methods
        return func
    return decorator

def batch(func):
    func.batch = True
    return func
