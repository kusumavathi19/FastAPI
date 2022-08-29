#one-to one
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
    __tablename__ = "table1"
    id = Column(Integer, primary_key=True)

    # previously one-to-many Parent.children is now
    # one-to-one Parent.child
    child = relationship("Child", back_populates="table1", uselist=False)


class Child(Base):
    __tablename__ = "table2"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("table1.id"))

    # many-to-one side remains, see tip below
    parent = relationship("Parent", back_populates="table2")
Base.metadata.create_all(engine) 
session  = SessionLocal()
session.commit()        


