from sharepass import app, db
import datetime

class Password(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    hash = db.Column(db.String(255), nullable=False, unique=True)
    cipher = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text)

    @staticmethod
    def get_by_hash(hash):
        return Password.query.filter_by(hash=hash).first()

    def __repr__(self):
        return "<Password '{}'>".format(self.hash)
