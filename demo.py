from flask import Flask
from flask_rest4 import Api, Resource, batch


app = Flask(__name__)
api = Api(app)

@api.route("/A/<a_id>/")
@api.route("/B/<a_id>/")
class A(Resource):
    def list(self):
        pass

    def create(self):
        pass

    def get(self, a_id):
        pass

    def update(self, a_id):
        pass

    def delete(self, a_id):
        pass

    def batch_delete(self):
        pass

    def delete_test_1(self, a_id):
        pass

    def delete_test_2(self, a_id):
        pass

    @batch
    def delete_test_3(self):
        pass

    def option(self, a_id):
        pass

    def options(self):
        pass

@api.route("/CE/<c_id>/")
@api.route("/C/<c_id>/")
def c_post(c_id):
    pass

@api.route("/C/<c_id>/", "PUT")
def c_put(c_id):
    pass

@api.route("/D/<d_id>/", "POST", "PUT")
def d_post_put(d_id):
    pass

@api.route("/e/<e_id>/", "POST", "PUT")
def e_post_put(e_id):
    pass

print(api)

app.run(host='0.0.0.0', port=8000, debug=True)
