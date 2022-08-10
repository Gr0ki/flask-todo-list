from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from ..extensions import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    tasks = relationship("Task", backref="users")
    last_login = Column(DateTime, default=datetime.now())

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
