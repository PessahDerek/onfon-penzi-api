from datetime import datetime

from ..extensions import db

class BaseModel:
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

class User(BaseModel, db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    county = db.Column(db.String(80), nullable=False)
    town = db.Column(db.String(80), nullable=False)
    # TODO: add details
