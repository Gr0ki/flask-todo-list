from datetime import datetime


from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from ..extensions import db


class Task(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    notes = Column(Text, nullable=True, default=None)
    is_done = Column(Boolean, default=False)
    updated_date_time = Column(DateTime, default=datetime.now())
