#This pprogram describes creation of another table which is related to already existing one in our database. 
# The customers table contains master data of customers. 
# We now need to create invoices table which may have any number of invoices belonging to a customer. 
#This is a case of one to many relationships.
import urllib
from sqlalchemy import create_engine,Column,ForeignKey ,Integer,Table, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import FastAPI, Form
engine=None
#connection
DB_URL = "oracle+cx_oracle://kusuma:kusuma@localhost:1521/xe"
engine = create_engine(DB_URL)
connection=engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()


class Customer(Base):
   __tablename__ = 'customers'

   id = Column(Integer, primary_key = True)
   name = Column(String(255))
   address = Column(String(255))
   email = Column(String(255))

class Invoice(Base):
   __tablename__ = 'invoices'
   
   id = Column(Integer, primary_key = True)
   custid = Column(Integer, ForeignKey('customers.id'))
   invno = Column(Integer)
   amount = Column(Integer)
   customer = relationship("Customer", back_populates = "invoices")

Customer.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "customer")
Base.metadata.create_all(engine)    
