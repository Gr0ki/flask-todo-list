from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..extensions import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    tasks = relationship("Task", backref="users")
    last_login = Column(DateTime, default=datetime.now())
