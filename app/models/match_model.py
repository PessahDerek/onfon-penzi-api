from ..extensions import db


class SentMatched(db.Model):
    __tablename__ = 'sent_matched'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    match_table_id = db.Column(db.Integer, db.ForeignKey('match_table.id'), nullable=False)

    # Define the back relationship to MatchTable
    match_table_ref = db.relationship('MatchTable', back_populates='sent')

    def dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "match_table_id": self.match_table_id,
        }


class PairTable(db.Model):
    __tablename__ = 'pairs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Person who sent the request
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Matched person
    match_table_id = db.Column(db.Integer, db.ForeignKey('match_table.id'))

    # Define a relationship to MatchTable using the class name
    match_table = db.relationship('MatchTable', back_populates='matches')

    def dict(self):
        return {
            "id": self.id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id,
            "match_table_id": self.match_table_id,
        }


class MatchTable(db.Model):
    __tablename__ = 'match_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)

    # Define a relationship to PairTable using the class name, with backref to PairTable
    matches = db.relationship('PairTable', back_populates='match_table', lazy='dynamic')

    # Define a relationship to SentMatched using the class name, with back_populates
    sent = db.relationship('SentMatched', back_populates='match_table_ref', lazy='dynamic')

    def dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "message_id": self.message_id,
            "matches": self.matches,
            "sent": self.sent.all()
        }
