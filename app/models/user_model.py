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

    def dict(self):
        return {
            "id": self.id,
            "description": self.description if self.description else "",
            "education": self.education if self.education else "",
            "profession": self.profession if self.profession else "",
            "marital_status": self.marital_status if self.marital_status else "",
            "religion": self.religion if self.religion else "",
            "ethnicity": self.ethnicity if self.ethnicity else "",
            "user_id": self.user_id if self.user_id else "",
        }


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

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "age": self.age,
            "gender": self.gender.name,
            "county": self.county,
            "town": self.town,
            "details": self.details[0].dict() if len(self.details) > 0 else None,
        }
