from db import db

# Model - Methods/utilities that enable the program to do what it needs to do
#         Internal represenation of the data

# Resource - Things the the API responds with: students, items, stores etc.
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        ''' Insert the current object to the database. Can do an
            update and insert. The session is a collection of obejects
            that can be written to the database'''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        ''' query database using username. this line will:
            SELECT * FROM users WHERE username=?" LIMIT 1
            which will return the first row returned
        '''
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):

        ''' query the database to do:
            "SELECT * FROM users WHERE id=?"
        '''
        return cls.query.filter_by(id=_id).first()
