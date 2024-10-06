from setup import db
from datetime import datetime


#################
# USER MODEL
#################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(350), nullable=False)
    email = db.Column(db.String(350), nullable=False, unique=True)
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
            'sign_up_date': self.created_at,
            'last_modified_date': self.updated_at
        }


#################
# SUBJECT MODEL
#################
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(350), nullable=False, unique=True)
    questions = db.relationship('Question', backref='subject')
    results = db.relationship('Result', backref='subject')

    def __init__(self, name:str):
        self.name = name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


#################
# QUESTION MODEL
#################
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer(), primary_key=True)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'))
    question = db.Column(db.String(350), nullable=False)
    option1 = db.Column(db.String(150), nullable=False)
    option2 = db.Column(db.String(150), nullable=False)
    option3 = db.Column(db.String(150), nullable=False)
    answer = db.Column(db.String(150), nullable=False)

    def __init__(self, subject_id:int, question:str, option1:str, 
                 option2:str, option3:str, answer:str):
        self.subject_id = subject_id
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.answer = answer

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'question': self.question,
            'option1': self.option1,
            'option2': self.option2,
            'option3': self.option3,
            'answer': self.answer
        }

    def __repr__(self) -> str:
        return f'<id: {self.id}, question:{self.question}, subject_id:{self.subject_id}>.'

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'))
    score = db.Column(db.Integer(), nullable=False)
    total_score = db.Column(db.Integer(), nullable=False) 
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, user_id:int, subject_id:int, score:int, total_score:int):
        self.user_id = user_id
        self.subject_id = subject_id
        self.score = score
        self.total_score = total_score
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'owner': self.user.to_json(),
            'subject': self.subject.to_json(),
            'score': self.score,
            'total_score': self.total_score,
            'created_at': self.created_at
        }

def create_db_tables(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    