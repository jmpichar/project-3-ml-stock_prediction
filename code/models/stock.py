from db import db

class StockModel(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.String(80))
    open_price = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)

    def __init__(self, name, date, open_price, close, volume):
        self.name = name
        self.date = date
        self.open_price = open_price
        self.close = close
        self.volume = volume

    def json(self):
        return {'name': self.name, 'date': self.date, 'open_price':self.open_price, 'close':self.close, 'volume':self.volume}

    @classmethod
    def find_by_name(cls, name):

        ''' The line:
            return StockModel.query.filter_by(name=name).first()
        performs:
        SELECT * FROM items WHERE name=name LIMIT 1
        Because its a class nethod we can use cls
        '''
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        ''' Insert the current object to the database. Can do an
            update and insert. The session is a collection of obejects
            that can be written to the database'''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        ''' delete an itemModel from the database. This will do:
            "DELETE FROM items WHERE name=?"
        '''
        db.session.delete(self)
        db.session.commit()

