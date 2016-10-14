# coding=utf-8
from __future__ import absolute_import

from flask import Flask

# from resource import Resource, make_cors_headers, Url, extend
from flask_rest4 import Resource, RESTful, extend, manage


def create_app():
    app = Flask(__name__)

    # @app.before_request
    # def app_before_request():
    #     # cors response
    #     if request.method == "OPTIONS":
    #         resp = current_app.make_default_options_response()
    #         cors_headers = make_cors_headers()
    #         resp.headers.extend(cors_headers)
    #         return resp

    return app


if __name__ == "__main__":
    app = create_app()
    restful = RESTful(app)

    @restful.register('/books/<book_id>')
    @extend(batch_get='GET')
    class book(Resource):
        def get(self, book_id):
            return [{
                'id': 1,
                'name': 'book1'
            }]

        def batch_get(self):
            return [{
                'id': 2,
                'name': 'book1'
            }]
    manage.list_routes(restful)

    app.run(debug=True, threaded=True, port=6002)
