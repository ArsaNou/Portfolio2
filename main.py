from flask import Flask, request, jsonify, make_response, after_this_request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)


prod_put_args = reqparse.RequestParser()
prod_put_args.add_argument("name", type=str, help="Name of the product", required=True)
prod_put_args.add_argument("number", type=int, help="Number of products")
prod_put_args.add_argument("price", type=int, help="Price of the products")


class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Integer, nullable=False)


products = {}



prod_put_args = reqparse.RequestParser()
prod_put_args.add_argument("name", type=str, help="Name of the product", required=True)
prod_put_args.add_argument("price", type=int, help="Price of products", required=True)
prod_put_args.add_argument("colors", type=int, help="Colors of the products", required=True)

prod_update_args = reqparse.RequestParser()
prod_update_args.add_argument("name", type=str, help="Name of the product")
prod_update_args.add_argument("price", type=int, help="Price of products")
prod_update_args.add_argument("colors", type=int, help="Colors of the products")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer,
    'colors': fields.Integer
}


class Products(Resource):
    @marshal_with(resource_fields)
    def get(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        result = ProductModel.query.all()
        if not result:
            abort(404, message="Could not find product with that id...")
        return result
        # return products[prod_id]


class Product(Resource):
    @marshal_with(resource_fields)
    def get(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        result = ProductModel.query.filter_by(id=prod_id).first()
        if not result:
            abort(404, message="Could not find product with that id...")
        return result
        # return products[prod_id]

    @marshal_with(resource_fields)
    def put(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        args = prod_put_args.parse_args()
        result = ProductModel.query.filter_by(id=prod_id).first()
        if result:
            abort(409, message="Product id taken...")

        product = ProductModel(id=prod_id, name=args['name'], price=args['price'], colors=args['colors'])
        db.session.add(product)
        db.session.commit()
        return product, 201
        # args = prod_put_args.parse_args()
        # products[prod_id] = args
        # return products[prod_id], 201

    @marshal_with(resource_fields)
    def patch(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = True
            response.headers['Access-Control-Allow-Methods'] = ["GET", "PUT", "PATCH"]
            response.headers['Access-Control-Allow-Headers'] = ["Origin", "Content-Type", "Accept"]
            return response

        args = prod_update_args.parse_args()
        result = ProductModel.query.filter_by(id=prod_id).first()
        if not result:
            abort(404, message="Could not find product with that id...")

        if args['name']:
            result.name = args['name']
        if args['price']:
            result.price = args['price']
        if args['colors']:
            result.colors = args['colors']
        # Remove?
        # db.session.add(result)
        db.session.commit()

        return result

    def delete(self, prod_id):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        abort_if_prod_id_doesnt_exist(prod_id)
        del products[prod_id]
        return '', 204



class Cart(Resource):
    cart = []



    def get(self):
        return self.cart

    def put(self, product):
        #Sjekke om produktet finnes i db
        #Bruke reqParser

        if product not in self.cart:
            self.cart.append(product)
            return '', 201
        else:
            return "Product is already in cart"
        # Kan jo ha flere av et produkt.??

    def delete(self, product):
        if product not in self.cart:
            return 400  # Bad Request
        else:
            for item in self.cart:
                if item == product:
                    self.cart.remove(item)
                    return 'product removed from cart', 200


api.add_resource(Cart, "/cart/etellerannet")
api.add_resource(Product, "/product/<int:prod_id>")
api.add_resource(Products, "/products")


if __name__ == '__main__':
    app.run(debug=True)
