#many-to-one
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

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("child.id"))
    child = relationship("Child", back_populates="parents")


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parents = relationship("Parent", back_populates="child")
Base.metadata.create_all(engine) 
session  = SessionLocal()
session.commit()