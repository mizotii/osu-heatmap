"""for reading from the database"""
from db.models import db, User

def read_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def all_users(app):
    with app.app_context():
        return User.query.all()