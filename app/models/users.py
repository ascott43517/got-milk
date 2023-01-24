from app import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String)
    username = db.Column(db.String)
    posts = db.relationship("Posts", back_populates="users", lazy=True)
