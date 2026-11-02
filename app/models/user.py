from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import base

class users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)