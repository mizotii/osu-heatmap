"""for reading from the database"""
from db.models import db, Token

def read_user(id):
    user = Token.query.filter_by(id=id).first()
    return user