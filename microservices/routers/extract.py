from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    password = Column(VARCHAR(255))


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    address = Column(VARCHAR(255))
    email = Column(VARCHAR(255))

    invoices = relationship('Invoices', back_populates='customers')


class Pets(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    age = Column(Integer)
    type = Column(VARCHAR(30))


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    password = Column(VARCHAR(255))


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    custid = Column(ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)

    customers = relationship('Customers', back_populates='invoices')
