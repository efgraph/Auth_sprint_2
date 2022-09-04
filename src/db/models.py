import enum
import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    func, Enum,
)
from sqlalchemy.dialects.postgresql import UUID

from db.config import db


class OAuthName(enum.Enum):
    google = 'google'


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class Role(db.Model, TimestampMixin):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(20), unique=True)
    description = Column(String(255))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = Column(BigInteger(), primary_key=True)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))


class User(db.Model, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_superuser = Column(Boolean(), default=False)


class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    user_agent = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())


class Password(db.Model):
    __tablename__ = 'passwords'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    password = Column(String(512), nullable=False)


class OAuthAccount(db.Model):
    __tablename__ = 'oauth_account'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    oauth_id = Column(String(255), nullable=False, unique=True)
    oauth_provider = Column(Enum(OAuthName), nullable=False)
