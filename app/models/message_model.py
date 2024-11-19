import enum
from datetime import datetime, timezone
from ..extensions import db
from sqlalchemy import Enum as AlchemyEnum


class MsgType(enum.Enum):
    outgoing = 'outgoing'
    incoming = 'incoming'

    # def readable(self):
    #     return self.name


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    msg_type = db.Column(AlchemyEnum(MsgType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'phone': self.phone,
            'message': self.message,
            'msg_type': self.msg_type.name,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f'<Message {self.message}>'
