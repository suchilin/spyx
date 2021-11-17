from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Hit(db.Model):

    __tablename__ = 'hits'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), unique=True, nullable=False)
    target = db.Column(db.String(128), nullable=False)
    hitman_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    hitman = db.relationship('User', foreign_keys="[Hit.hitman_id]")
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', foreign_keys="[Hit.creator_id]")
    status = db.Column(db.String(255), nullable=False, default="asigned")

    def __init__(self, description, target,hitman_id,creator_id):
        self.description = description
        self.target=target
        self.hitman_id=hitman_id
        self.creator_id=creator_id

    def __repr__(self):
        return f'<Hit {self.target}>'


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
