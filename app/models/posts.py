from app import db
import datetime

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    formula_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    address = db.Column(db.String)
    available = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    users = db.relationship("Users", back_populates="posts")
