from flask import Flask, request, jsonify, make_response, after_this_request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'
db = SQLAlchemy(app)


class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product(name={name}, price = {price}, colors = {colors})"


class PrevPurchased(db.Model):
    dato = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String(100), nullable=False)

# if not os.path.exists("tmp/database.db"):
#    db.create_all()


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
    now = date.now()

    def get(self):
        return self.cart

    @marshal_with(resource_fields)
    def put(self):
        @after_this_request
        def add_header(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        args = prod_put_args.parse_args()
        product = ProductModel.query.filter_by(id=args['prod_id']).first()
        if product:
            self.cart.append(product)
            return 'Added to cart', 201
        else:
            return "product could not be found???", 400

    def delete(self):
        args = prod_put_args.parse_args()

        for product in self.cart:
            if product.prod_id == args['prod_id']:
                self.cart.remove(product)
                return 'Product removed', 201
            else:
                return 'Could not remove', 409

    def calcPrice(self):
        price = 0
        for product in self.cart:
            price += product.price
        return price

    def purchase(self):
        items = "Items purchased: "
        price = self.calcPrice()
        dateofpurchase = self.now.strftime("%d/%m/%Y %H:%M:%S")

        for item in self.cart:
            items += item.name + ", "

        purchase = PrevPurchased(dato=dateofpurchase, price=price, items=items)

        db.session.add(purchase)
        db.session.commit()

        return 'Something...', 200


api.add_resource(Cart, "/cart/etellerannet")
api.add_resource(Product, "/product/<int:prod_id>")
api.add_resource(Products, "/products")

if __name__ == '__main__':
    app.run(debug=True)
