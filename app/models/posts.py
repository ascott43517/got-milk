from app import db

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    users = db.relationship("Users", back_populates="posts")
