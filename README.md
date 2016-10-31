Flask_REST4
---
Elegant RESTful API for  Flask apps.

``` python
from flask import Flask
from flask_rest4 import RESTful, Resource

app = Flask(__name__)
restful = RESTful(app)

@restful.route('/books/<book_id>')
class book(Resource):
    def list(self):
        pass

    def create(self):
        pass

    def get(self, book_id):
        pass

    def update(self, book_id):
        pass

    def delete(self, book_id):
        pass
```
Both work well with blueprint.
The resource will create an url map as following:

| route | methods | view function |
| --- | --- | --- |
| /books/ | GET | list |
| /books/ | POST | create |
| /books/`<book_id>`/ | GET | get |
| /books/`<book_id>`/ | PUT | update |
| /books/`<book_id>`/ | DELETE | delete |

INSTALL
---
```bash
pip install flask_rest4
```

EXTEND
---
If you want a simple `batch delete` api, add a simple batch delete view function.

``` python
@restful.route('/books/<book_id>')
class book(Resource):
    def list(self):
        pass

    def create(self):
        pass

    def get(self, book_id):
        pass

    def update(self, book_id):
        pass

    def delete(self, book_id):
        pass

    def batch_delete(self):
        pass
```

The url map has been updated as shown.

| route | methods | view function |
| --- | --- | --- |
| /books/ | GET | list |
| /books/ | POST | create |
| /books/batch_delete/ | POST | batch_delete |
| /books/`<book_id>`/ | GET | get |
| /books/`<book_id>`/ | PUT | update |
| /books/`<book_id>`/ | DELETE | delete |

If you want to set the methods of `batch delete` api as  `PUT`( The default value is `POST` ), use `extend` decorator

``` python
from flask_rest4 import RESTful, Resource, extend

@restful.route('/books/<book_id>')
@extend(batch_delete='PUT')
class book(Resource):
    def list(self):
        pass

    def create(self):
        pass

    def get(self, book_id):
        pass

    def update(self, book_id):
        pass

    def delete(self, book_id):
        pass

    def batch_delete(self):
        pass
```

COMMON API RESPOND WITH JSON DATA
---
``` python
from flask_rest4 import Api


app = Flask(__name__)
api = Api(app)

@api.route('/echo', 'GET')
def echo():
    pass
```

Or use `output_json` decorator with flask route
``` python
from flask_rest4.response import output_json

app = Flask(__name__)

@app.route('/echo', 'GET')
@output_json
def echo():
    pass
```