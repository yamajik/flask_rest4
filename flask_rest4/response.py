# coding=utf-8

import json
import functools

from flask import make_response

from .headers import make_cors_headers


def output_json(func):
    @functools.wraps(func)
    def decorate(*args, **kwargs):
        result = func(*args, **kwargs)
        data, status_code = load_result(result)
        return make_json_response(data, status_code or 200)

    return decorate


def load_result(result):
    if isinstance(result, tuple) and len(result) == 2:
        return result
    else:
        return result, 200


def make_json_response(data, status_code, headers=None):
    headers = headers or {}
    DEFAULT_HEADERS = {"Content-Type": "application/json"}
    headers.update(DEFAULT_HEADERS)
    headers.update(make_cors_headers(allowed_origins='*'))
    data = json.dumps(data)
    return make_response(data, status_code, headers)
