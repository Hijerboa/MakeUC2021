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

class TargetType(Base):
    __tablename__ = 'target_type'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class TargetSubType(Base):
    __tablename__ = 'target_sub_type'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class Nationality(Base):
    __tablename__ = 'nationality'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class WeaponType(Base):
    __tablename__ = 'weapon_type'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class WeaponSubtype(Base):
    __tablename__ = 'weapon_subtype'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(length=512), nullable=False)


class TargetInfo(Base, PrimaryKeyBase):
    __tablename__ = 'target_info'

    terror_act = Column(BigInteger(), ForeignKey('terrorist_act.id'))
    target_type = Column(Integer(), ForeignKey('target_type.id'))
    target_subtype = Column(Integer(), ForeignKey('target_sub_type.id'))
    target = Column(String(length=128))
    nationality = Column(Integer(), ForeignKey('nationality.id'))


class WeaponInfo(Base, PrimaryKeyBase):
    __tablename__ = 'weapon_info'

    terror_act = Column(BigInteger(), ForeignKey('terrorist_act.id'))
    weapon_type = Column(Integer(), ForeignKey('weapon_type.id'))
    weapon_subtype = Column(Integer(), ForeignKey('weapon_subtype.id'))


class PropertyDamageExtent(Base):
    __tablename__ = 'property_damage_extent'

    id = Column(Integer(), nullable=False, primary_key=True)
    description = Column(String(length=512), nullable=False)


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

    success = Column(Boolean())
    suicide = Column(Boolean())
    motive = Column(String(length=512))

    prop_dam = Column(Boolean())
    prop_dam_ext = Column(Integer(), ForeignKey('property_damage_extent.id'))
    prop_dam_value = Column(Integer())
    prop_comment = Column(String(length=1024))

    hostages = Column(Boolean())
    num_hostages = Column(Integer())
    num_hostages_us = Column(Integer())
    ransom = Column(Integer())
    ransom_amt = Column(Integer())

