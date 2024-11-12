from sqlalchemy import Enum as AlchemyEnum, ForeignKey
from ..extensions import db
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class Details(db.Model):
    __tablename__ = 'details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, unique=False, nullable=True)
    education = db.Column(db.String(100), unique=False, nullable=True)
    profession = db.Column(db.String(100), unique=False, nullable=True)
    marital_status = db.Column(db.String(100), unique=False, nullable=True)
    religion = db.Column(db.String(100), unique=False, nullable=True)
    ethnicity = db.Column(db.String(100), unique=False, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(AlchemyEnum(Gender), nullable=False, default=Gender.FEMALE)
    county = db.Column(db.String(50), unique=False, nullable=False)
    town = db.Column(db.String(50), unique=False, nullable=False)
    details = db.relationship('Details', backref='user_ref', lazy=True, cascade='all, delete-orphan')

