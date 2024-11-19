from ..extensions import db


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'userName': self.username,
            'password': self.password
        }

