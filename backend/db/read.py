"""for reading from the database"""
from db.models import db, User

def read_user(id):
    user = User.query.filter_by(id=id).first()
    return user