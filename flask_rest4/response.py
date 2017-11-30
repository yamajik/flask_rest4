# coding=utf-8

import json
import functools

from flask import make_response, current_app, request


def output_json(func):
    @functools.wraps(func)
    def decorate(*args, **kwargs):
        if not request.is_xhr:
            data = "This is not an ajax request."
            return make_response(data, 403, default_headers())
        result = func(*args, **kwargs)
        data, status_code = load_result(result)
        if not data and current_app.debug:
            data = {"message": "This is a debug message."}
        return make_json_response(data, status_code or 200)
    decorate.name = func.__name__
    return decorate


def load_result(result):
    if isinstance(result, tuple) and len(result) == 2:
        return result
    else:
        return result, 200


def make_json_response(data, status_code, headers=None):
    headers = headers or {}
    headers.update(default_headers())
    data = json.dumps(data)
    return make_response(data, status_code, headers)


@output_json
def default_option(*args, **kargs):
    return {"message": "I'm alive."}


def default_headers():
    headers = {}
    headers.update(ajax_headers())
    headers.update(cors_headers(allowed_origins='*'))
    return headers


def ajax_headers():
    return {"Content-Type": "application/json"}


def cors_headers(allowed_origins=None,
                 allowed_credentials=False,
                 max_age=86400):
    headers = dict()
    headers["Access-Control-Allow-Headers"] = _make_allow_headers()
    headers_options = "OPTIONS, HEAD, POST, PUT, DELETE"
    headers["Access-Control-Allow-Methods"] = headers_options

    if '*' in allowed_origins:
        headers["Access-Control-Allow-Origin"] = '*'
    elif request.headers.get('Origin') in allowed_origins:
        headers["Access-Control-Allow-Origin"] = request.headers['Origin']

    if allowed_credentials:
        headers["Access-Control-Allow-Credentials"] = 'true'

    headers["Access-Control-Max-Age"] = max_age
    return headers


def _make_allow_headers():
    request_allows = request.headers.get(
        "Access-Control-Request-Headers", None)
    if request_allows:
        return request_allows
    else:
        base_set = ["origin", "accept", "content-type", "authorization"]
        return ", ".join(base_set)
