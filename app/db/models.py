from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, UniqueConstraint, LargeBinary, \
    Table, DateTime, Date
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class PrimaryKeyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)

class TerroristAct(Base):
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer(), nullable=False)
    day = Column(Integer(), nullable=False)
    approx_date = Column(String(length=64), nullable=True)
