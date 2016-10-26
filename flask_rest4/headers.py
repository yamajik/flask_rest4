# coding=utf-8

from flask import request


def make_cors_headers(allowed_origins=None,
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
