'''Rest4 response helpers

Response helper functions for Rest4
'''


import functools
import json

from flask import current_app, make_response, request

from . import settings


def output_json(func):
    @functools.wraps(func)
    def decorate(*args, **kwargs):
        result = func(*args, **kwargs)
        data, status_code = load_result(result)
        if data is None and current_app.debug:
            data = settings.DEFAULT_DEBUG_MESSAGE_DATA.copy()
            data[settings.ENDPOINT_KEY_NAME] = str(func)
            status_code = 200
        return make_json_response(data, status_code or 200)
    return decorate


def load_result(result):
    if isinstance(result, tuple) and len(result) == 2:
        return result
    else:
        return result, 200 if result is not None else 204


def make_json_response(data, status_code, headers=None):
    headers = headers or {}
    headers.update(default_headers())
    data = safe_jsonify(data)
    return make_response(data, status_code, headers)


def safe_jsonify(data):
    try:
        return json.dumps(data) if data is not None else ""
    except:
        return str(data)


def default_headers():
    headers = settings.DEFAULT_HEADERS
    headers.update(ajax_headers())
    headers.update(cors_headers())
    return headers


def ajax_headers():
    return {"Content-Type": "application/json"}


def cors_headers():
    allow_headers = request.headers.get("Access-Control-Request-Headers",
                                        settings.CORS_HEADERS_ALLOW_HEADERS)
    allow_methods = settings.CORS_HEADERS_ALLOW_METHODS
    allowed_origins = settings.CORS_HEADERS_ALLOW_ORIGIN
    if '*' in allowed_origins:
        allowed_origins = '*'
    elif request.headers.get('Origin') in allowed_origins:
        allowed_origins = request.headers['Origin']
    allow_credentials = str(settings.CORS_HEADERS_ALLOW_CREDENTIALS).lower()
    max_age = settings.CORS_HEADERS_MAX_AGE

    return {
        "Access-Control-Allow-Headers": allow_headers,
        "Access-Control-Allow-Methods": allow_methods,
        "Access-Control-Allow-Origin": allowed_origins,
        "Access-Control-Allow-Credentials": allow_credentials,
        "Access-Control-Max-Age": max_age
    }
