from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import MainBase


class Donation(MainBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
