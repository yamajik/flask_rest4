from flask import Flask
from flask_rest4 import Api, Resource, batch, alias


app = Flask(__name__)
api = Api(app)


# register resource endpoint

@api.route("/A/<a_id>/")
@api.route("/A2/<a_id>/")
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

    # keyword "batch" specifies this action as a batch action
    def batch_delete(self):
        pass

    def action1(self, a_id):
        pass

    def action2(self, a_id):
        pass

    # specifies this action as a batch action
    @batch
    def action3(self):
        pass

    # override default OPTION method for "/A/<a_id>/"
    def option(self, a_id):
        pass

    # override default OPTION method for "/A/"
    def options(self):
        pass


# add common api endpoint

@api.route("/C/<c_id>/")
@api.route("/C2/<c_id>/")
def c_post(c_id):
    pass

@api.route("/C/<c_id>/", "PUT")
def c_put(c_id):
    pass

@api.route("/D/<d_id>/", "POST", "PUT")
def d_post_put(d_id):
    pass

@api.route("/E/<e_id>/", "POST", "PUT")
def e_post_put(e_id):
    pass


if __name__ == '__main__':
    print(api)
    app.run(host='0.0.0.0', port=8000, debug=True)
