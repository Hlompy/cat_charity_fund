from sqlalchemy import Column, String, Text

from .base import MainBase


class CharityProject(MainBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
