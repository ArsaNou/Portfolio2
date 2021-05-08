import flask

app = flask.Flask(__name__)


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




if __name__ == '__main__':
    app.run(debug=True)



# TEST TWO
