from project import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
