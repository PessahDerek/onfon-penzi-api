"""
Define all models
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import Enum, false, Column, Integer, ForeignKey
from sqlalchemy.orm import Relationship, Mapped, declarative_base, relationship

from .extensions import db


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class MessageEnum(enum.Enum):
    outgoing = "outgoing"
    incoming = "incoming"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(Enum(GenderEnum), nullable=False)
    county = db.Column(db.String(50), unique=False, nullable=False)
    town = db.Column(db.String(50), unique=False, nullable=False)
    details = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"


class Detail(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    education = db.Column(db.String(100), nullable=True)
    profession = db.Column(db.String(100), nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    religion = db.Column(db.String(50), nullable=True)
    ethnicity = db.Column(db.String(50), nullable=True)
    user: Mapped[User] = Relationship(back_populates="details")


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)
    msg_type = db.Column(Enum(MessageEnum), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))


class SentMatch(db.Model):
    __tablename__ = "sent_matches"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=False)


base = declarative_base()

PairTable = db.Table(
    'pairs',
    base.metadata,
    Column('match_user_id', Integer, ForeignKey(User.id)),
    Column('match_table_id', Integer, ForeignKey("matches.id")),
)


class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=False)
    matches = relationship('User', secondary=PairTable, backref="users")


