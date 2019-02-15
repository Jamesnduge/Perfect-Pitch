from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class Review:

    all_reviews = []

    def __init__(self,pitch_id,title,pitch,review):
        self.pitch_id = pitch_id
        self.title = title
        self.pitch = pitch
        self.review = review

    def save_review(self):
        Review.all_reviews.append(self)


    @classmethod
    def get_reviews(cls,id):

        response = []

        for review in cls.all_reviews:
            if review.pitch_id == id:
                response.append(review)

        return response

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    # password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure=db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = password


    # def verify_password(self,password):
    #     return check_password_hash(self.pass_secure,password)
    #
    # def __repr__(self):
    #     return f'User {self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'
