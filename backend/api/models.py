# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime

import json
from sqlalchemy import text

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.Text())
    jwt_auth_active = db.Column(db.Boolean())
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)
    uploads = db.relationship('Upload', backref='users', lazy=True)
    roles = db.Column(db.String(), default='', server_default=text("''"))

    def __repr__(self):
        return f"User {self.username}"
    
    def __init__(self, username, email, password, roles=None):
        self.username = username
        self.email = email
        self.set_password(password)
        # ... your existing constructor logic ...
        if roles is None:
            roles = []
        self.roles = ','.join(roles)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_email(self, new_email):
        self.email = new_email

    def update_username(self, new_username):
        self.username = new_username

    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def has_role(self, role):
        return role in self.roles.split(',')
    
    def set_roles(self, roles):
        self.roles = ','.join(roles)
    
    def get_roles(self):
        return self.roles.split(',')

    def toDICT(self):
        print(self.roles)
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': self.roles.split(','),
        }

    def toJSON(self):

        return self.toDICT()


class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CalculatedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()