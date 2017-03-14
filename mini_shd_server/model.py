
from settings import DBPath, DBEcho
from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, ForeignKey, Unicode, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine(DBPath, echo=DBEcho)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata


class Pull(DeclarativeBase):

    """ Pull """

    __tablename__ = 'pull'

    id = Column(Integer, primary_key=True, autoincrement=True)
    md5 = Column(Unicode(256), nullable=False, unique=True)
    obj = Column(PickleType, nullable=False)
    files = relationship('File')


class File(DeclarativeBase):

    """ File """

    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(512), nullable=False)
    pull_id = Column(Integer, ForeignKey('pull.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class User(DeclarativeBase):

    """ User """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(256), nullable=False, unique=True)
    passwd = Column(Unicode(512))
    files = relationship('File')


# Calculated Column
from sqlalchemy.orm import column_property
from sqlalchemy import select

File.uname = column_property(select([(User.name)], File.user_id == User.id))
File.md5 = column_property(select([(Pull.md5)], File.pull_id == Pull.id))
File.obj = column_property(select([(Pull.obj)], File.pull_id == Pull.id))

# Create Database
metadata.create_all()
