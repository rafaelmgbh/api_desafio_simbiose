from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    user_type = Column(Integer)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    picture = Column(String)


class Papers(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String)
    title = Column(String)
    summary = Column(String)
    body = Column(String)
    firstParagraph = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
