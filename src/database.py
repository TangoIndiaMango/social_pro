from datetime import datetime
from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import string
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    profilePic = db.Column(db.Text(), default="Image Should be Uploaded")
    password = db.Column(db.Text(), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    post = db.relationship('Post', backref="user")
    comment = db.relationship('Comment', backref="user")

    def __repr__(self):
        return  f'Username: {self.username}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text(), nullable=True)
    image = db.Column(db.Text(), default="Image Should be Uploaded")
    likes = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    comment = db.relationship('Comment', backref="post")

    def __repr__(self):
        return  f'Username: {self.message}'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text(), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    likes = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return  f'Comment: {self.comment}'