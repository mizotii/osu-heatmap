from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)


class APIToken(db.Model):
    __tablename__ = "api_tokens"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, autoincrement=True, primary_key=True)
    access_id = db.Column(db.Text(length=10000), nullable=False)
    refresh_id = db.Column(db.Text(length=10000), nullable=False)