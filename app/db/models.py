from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, UniqueConstraint, LargeBinary, \
    Table, DateTime, Date
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class PrimaryKeyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=128), nullable=False)


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=128), nullable=False)


class ProvState(Base):
    __tablename__ = 'prov_state'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=128), nullable=False)


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=128), nullable=False)


class Specificity(Base):
    __tablename__ = 'specificity'

    id = Column(Integer(), nullable=False, primary_key=True)
    description = Column(String(length=512), nullable=False)


class TerroristAct(Base):
    __tablename__ = 'terrorist_act'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer(), nullable=False)
    day = Column(Integer(), nullable=False)
    approx_date = Column(String(length=64), nullable=True)
    extended = Column(Boolean(), nullable=False)
    resolution = Column(Integer(), nullable=True)
    country = Column(Integer(), ForeignKey('country.id'))
    region = Column(Integer(), ForeignKey('region.id'))
    prov_state = Column(Integer(), ForeignKey('prov_state.id'))
    city = Column(Integer(), ForeignKey('city.id'))
    latitude = Column(Float(), nullable=False)
    longitude = Column(Float(), nullable=False)
    specificity = Column(Integer(), ForeignKey('specificity.id'), nullable=False)

