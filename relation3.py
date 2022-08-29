#many-to-many
import urllib
from sqlalchemy import create_engine,Column,ForeignKey ,Integer,Table, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI
engine=None
#connection
DB_URL = "oracle+cx_oracle://kusuma:kusuma@localhost:1521/xe"
engine = create_engine(DB_URL, echo = True)
connection=engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("left_id", ForeignKey("left.id")),
    Column("right_id", ForeignKey("right.id")),
)


class Parent(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    children = relationship("Child", secondary=association_table)


class Child(Base):
    __tablename__ = "right"
    id = Column(Integer, primary_key=True)
Base.metadata.create_all(engine) 
session  = SessionLocal()
session.commit()    