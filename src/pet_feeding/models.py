import enum
import hashlib
import logging
import os

from asyncpg import UniqueViolationError
from gino import Gino
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import contextlib

PASSWORD = os.environ['PASSWORD']
USER = os.environ['USER']
DB_NAME = os.environ['DB']
HOST = os.environ['HOST']

db = Gino()

LOG = logging.getLogger(__name__)


class BaseModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    def __str__(self):
        return f'{self.__tablename__}: {self.id}'

    def __repr__(self):
        return f'{self.__tablename__}: {self.id}'


# User part

class Groups(enum.Enum):
    super_admin = 1
    org_admin = 2


class OrgUser(BaseModel):
    __tablename__ = 'org_user'

    name = db.Column(db.Unicode(), nullable=False)
    password = db.Column(db.Unicode(), nullable=False)
    login = db.Column(db.Unicode(), unique=True, nullable=False)
    group = db.Column(db.Enum(Groups), nullable=False, default=Groups.org_admin)
    organization_id = db.Column(db.Integer(), db.ForeignKey('organization.id'))
    user = relationship("Organization", back_populates="user")


class AdminUser(BaseModel):
    __tablename__ = 'admin_user'
    name = db.Column(db.Unicode(), nullable=False)
    password = db.Column(db.Unicode(), nullable=False)
    login = db.Column(db.Unicode(), unique=True, nullable=False)
    group = db.Column(db.Enum(Groups), nullable=False, default=Groups.super_admin)


# END Users part


# Organization part


class Organization(BaseModel):
    __tablename__ = 'organization'

    name = db.Column(db.Unicode(), nullable=False)
    info = db.Column(JSONB, default='{}')
    user = relationship("OrgUser", back_populates="user")
    pet = relationship("Pet", back_populates="pet")
    meal = relationship("Meal", back_populates="meal")


# END Organization part


class Meal(BaseModel):
    __tablename__ = 'meal'

    name = db.Column(db.Unicode(), nullable=False)
    country = db.Column(db.Unicode(), nullable=False)
    info = db.Column(JSONB, default='{}')
    amount = db.Column(db.Float(), nullable=False)


class Pet(BaseModel):
    __tablename__ = 'pet'

    name = db.Column(db.Unicode(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    info = db.Column(JSONB, default='{}')
    org = relationship("Organization", back_populates="org")


class PetFeeding(BaseModel):
    __tablename__ = 'pet_feeding'

    time = db.Column(db.DateTime())


async def main():
    await db.set_bind(f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}')
    await db.gino.create_all()
    try:
        await AdminUser.create(name='Admin', password='3edc$RFV', login='admin@admin.com')
    except UniqueViolationError:
        LOG.error(f'Admin user already exist))')
    await db.pop_bind().close()


@contextlib.asynccontextmanager
async def conn():
    await db.set_bind(f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}')
    await db.gino.create_all()
    yield db.bind
    await db.pop_bind().close()
