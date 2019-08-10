from flask import render_template, request, redirect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.stock import StockModel
from models.stock import StockModel
from models.stock_prediction import *
from alpha_vantage.timeseries import TimeSeries
api_key = 'S7MZO4XSG71DN2NB'
# api works with resources and the resource has to be a class
# define the Stock resource
class Stock(Resource):
    TABLE_NAME = 'stocks'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    # parser.add_argument('date',
    #     type=str,
    #     required=True,
    #     help="This field cannot be left blank"
    # )
    #
    # parser.add_argument('open_price',
    #     type=float,
    #     required=True,
    #     help="This field cannot be left blank"
    # )
    #
    # parser.add_argument('close',
    #     type=float,
    #     required=False,
    #     help=""
    # )
    #
    # parser.add_argument('volume',
    #     type=float,
    #     required=True,
    #     help="This field cannot be left blank"
    # )


    def get(self, name):
        stock = StockModel.find_by_name(name)
        if stock:
            return stock.json()
        return {'message': 'Stock not found'}, 404

    def post(self, name):
        data = Stock.parser.parse_args()

        # not getting the name correctly from the url
        name = data["name"]
        print(f'Looking for ticker: {name}')

        if StockModel.find_by_name(name):
            return {'message': f'A stock with name {name} already exists'}, 400

        # data = Stock.parser.parse_args()
        # date = data['date']
        # open_price = data["open_price"]
        # close = data["open_price"]
        # volume = data["volume"]
        outcomes = get_stock_data(name)
        print(outcomes[0])
        for outcome in outcomes:
            # print(outcome)
            name = outcome['name']
            date = outcome['date']
            open_price = outcome['open_price']
            close = outcome['close']
            volume = outcome['volume']

            stock = StockModel(name=name, date=date, open_price=open_price, close=close, volume=volume)

            try:
                stock.save_to_db()
            except:
                raise
                return {'message':'an error occurred inserting the hand.'}, 500

        # print(f'{name}:{date}:{open_price}:{close}{volume}')

        try:
            stock.save_to_db()
        except:
            #raise
            return {'message':'an error occurred inserting the stock.'}, 500

        #return stock.json(), 201

        return redirect("/", code=302)

    def delete(self, name):
        stock = StockModel.find_by_name(name)

        if stock:
            item.delete_from_db()

        return {'message':'Stock deleted'}

    def put(self, name):
        data = Stock.parser.parse_args()

        # not getting the name correctly from the url
        name = data["name"]

        stock = StockModel.find_by_name(name)

        # StockModel.insert(stock)
        if stock:
            # update attributes
            stock.date = data['date']
            stock.open_price = data["open_price"]
            stock.volume = data["volume"]
        else:
            stock = StockModel(name=name, date=date, open_price=open_price, close=close, volume=volume)

        stock.save_to_db()

        return stock.json()

class StockList(Resource):
    def get(self):
        ''' query the database for all items. the query will perform
            the following SQL command:
                SELECT * FROM items
            Can be done using a list comprehesion or a lambda function:
            return {'stocks': list(map(lambda x: x.json() , StockModel.query.all()))}
        '''
        return {'stocks':[stock.json() for stock in StockModel.query.all()]}
        #return {[stock.json() for stock in StockModel.query.all()]}
