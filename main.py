from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse, abort
form flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = r'mysql+pymysql://root:{@localhost/users'
app.config['SECRET KEY'] = "secret phrase"
db = SQLAlchemy(app)


prod_put_args = reqparse.RequestParser()
prod_put_args.add_argument("name", type=str, help="Name of the product", required = True)
prod_put_args.add_argument("number", type=int, help="Number of products")
prod_put_args.add_argument("price", type=int, help="Price of the products")

products = {}

def abort_if_prod_id_doesnt_exist(prod_id):
    if prod_id not in products:
        abort(404, message="Product id is not valid...")

def abort_if_prod_id_exists():
    if prod_id in products:
        abort(409, message="Product already exists with that ID...")

class Prod(Resource):
    def get(self, prod_id):
        return products[prod_id]

    def put(self, prod_id):
        args = prod_put_args.parse_args()
        products[prod_id] = args
        return products[prod_id], 201

    def delete(self, prod_id):
        abort_if_prod_id_doesnt_exist(prod_id)
        del products[prod_id]
        return '', 204

api.add_resource(Prod, "/product/<int:prod_id>")

class Product:
    def __init__(self, productname, productprice):
        self.productname = productname
        self.productprice = productprice

    def getproductname(self):
        return self.productname

    def setproductname(self, nprodname):
        self.productname = nprodname

    def getprice(self):
        return self.productprice

    def setprice(self, nprice):
        self.productprice = nprice

class Cart:
    pass



if __name__ == '__main__':
    app.run(debug=True)



# TEST TWO
