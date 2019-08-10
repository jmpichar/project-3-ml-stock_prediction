from flask import Flask, render_template, request, redirect
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.stock import Stock, StockList
from sqlalchemy import create_engine

# from alpha_vantage import alpha_vantage.timeseries
from alpha_vantage.timeseries import TimeSeries
api_key = 'S7MZO4XSG71DN2NB'



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# turn off flask sqlalchemy tracker
# will sqlalchemy tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    return render_template("form.html")

@app.before_first_request
def create_tables():
    db.create_all()

# @app.route("/get_stock_data", methods=["POST"])
# def get_stock_data(ticker):
#     ts = TimeSeries(key=api_key,output_format='pandas')
#     # ticker = 'NASDAQ:INTC'
#
#     # Get the raw dataset
#     orig_dataset, meta_df = ts.get_daily(symbol=ticker, outputsize='full')
#
#     # Rename columns
#     orig_dataset.columns = ['open', 'high', 'low', 'close', 'volume']
#
#     engine = create_engine('sqlite:///data_tst.db', echo=False)
#     df.to_sql('test', con=engine)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Stock, '/stock/<string:name>')
api.add_resource(StockList, '/stocks')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
