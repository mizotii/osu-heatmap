from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, db.ForeignKey('api_tokens.user_id'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)


class APIToken(db.Model):
    __tablename__ = "api_tokens"

    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    access_id = db.Column(db.Text(length=2000), nullable=False)
    refresh_id = db.Column(db.Text(length=2000), nullable=False)