# from db import db
from datetime import datetime

# from .auth_route_funs import db

db=None

#################
# USER MODEL
#################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(350), nullable=False)
    email = db.Column(db.String(350), nullable=False)
    password = db.Column(db.String(350), nullable=False)
    results = db.relationship('Result', backref='user')
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now)


    def __init__(self, fullname:str, email:str, password:str):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'results': [result.to_json() for result in self.results],
            'sign_up_date': self.created_at,
            'last_modified_date': self.updated_at
        }
