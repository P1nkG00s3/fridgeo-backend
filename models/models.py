from datetime import datetime

from sqlalchemy import MetaData, JSON, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('role', String, nullable=False),
    Column('permissions', JSON),
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    #Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey(role.c.id)),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('sex', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False,nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)

