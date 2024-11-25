from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Group(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    permissions = relationship("Permission", backref="role")


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    group = Column(Integer, ForeignKey('role.id'), nullable=True)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    role = relationship("Group", backref="users")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    