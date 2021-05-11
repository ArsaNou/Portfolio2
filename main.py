from flask import Flask, url_for, send_from_directory, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import logging
import cgitb

cgitb.enable()
import os
import sys

# app config settings
app = Flask(__name__)

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# db connection you need to change here
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root://Something@localhost/lays'

# db settings and table handling ,change table here according to your db structure
db = SQLAlchemy(app)
images_table = db.Table('images', db.metadata, autoload=True, autoload_with=db.engine)
logo_count_table = db.Table('logo_count', db.metadata, autoload=True, autoload_with=db.engine)
test_table = db.Table('test_table', db.metadata, autoload=True, autoload_with=db.engine)
shop_table = db.Table('shop', db.metadata, autoload=True, autoload_with=db.engine)
rack_size_table = db.Table('rack_size', db.metadata, autoload=True, autoload_with=db.engine)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))


# getAll Apis
@app.route('/getAll', methods=['GET'])
def getAll():
    result = {}
    result["error"] = False
    rackData = db.session.query(rack_size_table).all()
    if rackData:
        result["data"] = rackData
        result['message'] = "Products Found."
    else:
        result['message'] = "Products Not Found."
        result["data"] = None
    response = app.response_class(
        response=json.dumps(result, sort_keys=False),
        mimetype='application/json',
        status=200
    )
    return response


# getproduct Apis
@app.route('/getproduct', methods=['GET'])
def getproduct():
    result = {}
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        result["error"] = True
        result['message'] = "Products Not Found."
        result["data"] = None
        response = app.response_class(
            response=json.dumps(result, sort_keys=False),
            mimetype='application/json',
            status=200
        )
        return response
    result["error"] = False
    rackData = db.session.query(rack_size_table).first()
    if rackData:
        result["data"] = rackData
        result['message'] = "Products Found."
    else:
        result['message'] = "Products Not Found."
        result["data"] = None
    response = app.response_class(
        response=json.dumps(result, sort_keys=False),
        mimetype='application/json',
        status=200
    )
    return response


# GetCart
@app.route('/getCart', methods=['GET'])
def getCart():
    result = {}
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        result["error"] = True
        result['message'] = "Cart Data Not Found."
        result["data"] = None
        response = app.response_class(
            response=json.dumps(result, sort_keys=False),
            mimetype='application/json',
            status=200
        )
        return response
    result["error"] = False
    rackData = db.session.query(rack_size_table).first()
    if rackData:
        result["data"] = rackData
        result['message'] = "Cart Data Found."
    else:
        result['message'] = "Cart Not Found."
        result["data"] = None
    response = app.response_class(
        response=json.dumps(result, sort_keys=False),
        mimetype='application/json',
        status=200
    )
    return response


# addtoCart Apis
@app.route('/addtoCart', methods=['POST'])
def addtoCart():
    if request.method == 'POST':
        product_id = request.form['product_id']
        # your table of cart where you need to u=insert add to cart data
        cartData = db.session.execute(
            images_table.insert().values(image_path=saved_path_1, result_image=saved_path_2, shop_id=shop_id,
                                         user_id=user_id, planogram=planogram, planogram_size=planogram_size,
                                         planogram_compliance=planogram_compliance, dateTime=todayTime,
                                         uploaded_date=todayDate, unique_id=unique_id, front_facia=frontFascia))
        db.session.commit()
        # to get last inserted id
        cart_id = cartData.lastrowid
        result = {}
        result["error"] = False
        result['message'] = "Data Added Successfully"
        result["data"] = None
        response = app.response_class(
            response=json.dumps(result, sort_keys=False),
            mimetype='application/json',
            status=200
        )
    else:
        result = {}
        result["error"] = True
        result['message'] = "Invalid Request."
        result["data"] = None
        response = app.response_class(
            response=json.dumps(result, sort_keys=False),
            mimetype='application/json',
            status=200
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port="5007")
