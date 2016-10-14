# coding=utf-8

from flask import Flask
from flask_rest4 import RESTful, Resource


app = Flask(__name__)
restful = RESTful(app)


@restful.route('/books/<book_id>')
class book(Resource):
    def list(self):
        return [{
            'id': 1,
            'name': 'book'
        }]

    def create(self):
        return {
            'id': 1,
            'name': 'book'
        }

    def get(self, book_id):
        return {
            'id': 1,
            'name': 'book'
        }

    def update(self, book_id):
        return {
            'id': 1,
            'name': 'book'
        }

    def delete(self, book_id):
        return {
            'id': 1
        }


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8000)
