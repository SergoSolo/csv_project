from sqlalchemy import ARRAY, Column, Integer, String

from app.core.db import Base


class Document(Base):
    name = Column(String(100), unique=True, nullable=False)
    columns = Column(ARRAY(String), nullable=False)
    size = Column(Integer, nullable=False)
    path = Column(String(200), unique=True)
