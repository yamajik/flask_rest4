from flask import Flask
from flask_rest4 import Api, Resource, batch, alias


app = Flask(__name__)
api = Api(app)


@api.route("/users/<user_id>/")
class User(Resource):
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


if __name__ == '__main__':
    print(api)
    app.run(host='0.0.0.0', port=8000, debug=True)
