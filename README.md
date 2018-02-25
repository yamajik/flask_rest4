# Flask_REST4

Elegant RESTful API for Flask apps.

``` python
from flask import Flask
from flask_rest4 import Api, Resource, batch, alias

app = Flask(__name__)
api = Api(app)

@api.route("/users/<user_id>/")
class User(Resource):
    def list(self):
        pass

    def create(self):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass
```

The resource will create an url map as following:

| route               | methods | view function |
| ------------------- | ------- | ------------- |
| /users/             | GET     | list          |
| /users/             | POST    | create        |
| /users/`<user_id>`/ | GET     | get           |
| /users/`<user_id>`/ | PUT     | update        |
| /users/`<user_id>`/ | DELETE  | delete        |

## INSTALL

```bash
pip install flask_rest4
```

## MUCH MORE

Let do some improved work for the User Api:
1. Use `register` instead of `create`
2. Add `login` api
3. Add `batch_delete` api
4. Add `invite` api

### alias *register* as *create* with `alias` decorator

``` python
from flask import Flask
from flask_rest4 import Api, Resource, alias

app = Flask(__name__)
api = Api(app)

@api.route('/users/<user_id>')
class user(Resource):
    def list(self):
        pass

    # use the rule as create
    @alias("create")
    def register(self):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass
```

The url map has been updated as shown.

| route               | methods | view function |
| ------------------- | ------- | ------------- |
| /users/             | GET     | list          |
| /users/             | POST    | register      |
| /users/`<user_id>`/ | GET     | get           |
| /users/`<user_id>`/ | PUT     | update        |
| /users/`<user_id>`/ | DELETE  | delete        |

### Add *login* api for url */users/* (Batch Api) with `batch` decorator

``` python
from flask import Flask
from flask_rest4 import Api, Resource, alias, batch

app = Flask(__name__)
api = Api(app)

@api.route('/users/<user_id>')
class user(Resource):
    def list(self):
        pass

    # use the rule as create
    @alias("create")
    def register(self):
        pass

    # specify this action as a batch action
    @batch
    def login(self):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass
```

The url map has been updated as shown.

| route               | methods | view function |
| ------------------- | ------- | ------------- |
| /users/             | GET     | list          |
| /users/             | POST    | register      |
| /users/             | PUT     | extras        |
|                     |         | - login       |
| /users/`<user_id>`/ | GET     | get           |
| /users/`<user_id>`/ | PUT     | update        |
| /users/`<user_id>`/ | DELETE  | delete        |

*login* is under control of *extras(batch action controller)*

### Add *batch_delete* to *extras(batch action controller)*

``` python
from flask import Flask
from flask_rest4 import Api, Resource, alias, batch

app = Flask(__name__)
api = Api(app)

@api.route('/users/<user_id>')
class user(Resource):
    def list(self):
        pass

    # use the rule as create
    @alias("create")
    def register(self):
        pass

    # specify this action as a batch action
    @batch
    def login(self):
        pass

    # keyword "batch" specifies this action as a batch action
    def batch_delete(self):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass
```

The url map has been updated as shown.

| route               | methods | view function  |
| ------------------- | ------- | -------------- |
| /users/             | GET     | list           |
| /users/             | POST    | register       |
| /users/             | PUT     | extras         |
|                     |         | - login        |
|                     |         | - batch_delete |
| /users/`<user_id>`/ | GET     | get            |
| /users/`<user_id>`/ | PUT     | update         |
| /users/`<user_id>`/ | DELETE  | delete         |


### Add *invite* api for url */users/<user_id>/* without anything

``` python
from flask import Flask
from flask_rest4 import Api, Resource, alias, batch

app = Flask(__name__)
api = Api(app)

@api.route('/users/<user_id>')
class user(Resource):
    def list(self):
        pass

    # use the rule as create
    @alias("create")
    def register(self):
        pass

    # specify this action as a batch action
    @batch
    def login(self):
        pass

    # keyword "batch" specifies this action as a batch action
    def batch_delete(self):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass

    def invite(self, user_id):
        pass
```

The url map has been updated as shown.

| route               | methods | view function  |
| ------------------- | ------- | -------------- |
| /users/             | GET     | list           |
| /users/             | POST    | register       |
| /users/             | PUT     | extras         |
|                     |         | - login        |
|                     |         | - batch_delete |
| /users/`<user_id>`/ | GET     | get            |
| /users/`<user_id>`/ | PUT     | update         |
| /users/`<user_id>`/ | DELETE  | delete         |
| /users/`<user_id>`/ | POST    | extra          |
|                     |         | - invite       |

*extra* is a action controller the same as *extras*

## COMMON API RESPOND WITH JSON DATA

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

## FLASK_REST4 IS FULL SUPPORT FOR *FLASK BLUEPRINT*

``` python
from flask_rest4 import Api

app = Flask(__name__)
blueprint = Blueprint('blueprint', __name__)
app.register_blueprint(blueprint)
api = Api(blueprint)

@api.route('/echo', 'GET')
def echo():
    pass
```

## CHECKOUT FOR MORE FEATURES

- [example.py](https://github.com/SquirrelMajik/flask_rest4/blob/master/example.py)
- [features.py](https://github.com/SquirrelMajik/flask_rest4/blob/master/features.py)
- demos
    - [Tip](https://github.com/SquirrelMajik/tip-server)
