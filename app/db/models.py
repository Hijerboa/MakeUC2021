from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Float, UniqueConstraint, LargeBinary, \
    Table, DateTime, Date, BigInteger
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


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class AlternativeDesignation(Base):
    __tablename__ = 'alt_designation'

    id = Column(Integer(), nullable=False, primary_key=True)
    description = Column(String(length=64), nullable=False)


class AttackType(Base):
    __tablename__ = 'attack_type'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)

class TerroristAct(Base):
    __tablename__ = 'terrorist_act'

    id = Column(BigInteger(), primary_key=True)
    date = Column(Date(), nullable=False)
    approx_date = Column(String(length=64), nullable=True)
    extended = Column(Boolean(), nullable=False)
    resolution = Column(Date(), nullable=True)
    country = Column(Integer(), ForeignKey('country.id'))
    region = Column(Integer(), ForeignKey('region.id'))
    prov_state = Column(Integer(), ForeignKey('prov_state.id'))
    city = Column(Integer(), ForeignKey('city.id'))
    latitude = Column(Float(), nullable=False)
    longitude = Column(Float(), nullable=False)
    specificity = Column(Integer(), ForeignKey('specificity.id'), nullable=False)
    vicinity = Column(Boolean(), nullable=True)
    location = Column(Integer(), ForeignKey('location.id'), nullable=True)
    summary = Column(String(length=4096), nullable=True)
    doubt_terrorism = Column(Boolean(), nullable=True)
    alt_designation = Column(Integer(), ForeignKey('alt_designation.id'))
    part_of_multiple = Column(Boolean())

    num_killed = Column(Integer())
    num_killed_us = Column(Integer())
    num_injured = Column(Integer())
    num_injured_us = Column(Integer())
    num_perp_killed = Column(Integer())
    num_perp_wounded = Column(Integer())