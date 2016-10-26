# coding=utf-8


DEFAULT_METHODS = {
    'get': 'GET',
    'list': 'GET',
    'create': 'POST',
    'update': 'PUT',
    'delete': 'DELETE'
}

DEFAULT_ENDPOINTS = DEFAULT_METHODS.keys()


def METHOD(methods, name):
    return methods.get(name, 'POST')
