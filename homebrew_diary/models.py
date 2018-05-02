from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from homebrew_diary import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actual_name = db.Column(db.String(128), default='N/a')
    favourite_styles = db.Column(db.String(128), default='beer')
    about = db.Column(db.String(2048), default='I like beer.')
    contact = db.Column(db.String(128), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128))
    style = db.Column(db.String(128))
    ingredients = db.Column(db.String(2048))
    method = db.Column(db.String(8192))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('recipes', lazy=True))


class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brewed_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(8192))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe', backref=db.backref('brews', lazy=True))    
    brewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brewer = db.relationship('User', backref=db.backref('brews', lazy=True))


class Tasting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tasted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128))
    comment = db.Column(db.String(4096))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = db.relationship('Recipe', backref=db.backref('tastings', lazy=True))    
    brew_id = db.Column(db.Integer, db.ForeignKey('brew.id'))
    brew = db.relationship('Brew', backref=db.backref('tastings', lazy=True))
    taster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    taster = db.relationship('User', backref=db.backref('tastings', lazy=True))    


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('activity', lazy=True))
    