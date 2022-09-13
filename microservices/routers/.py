from sqlalchemy import Column, ForeignKey, Integer, Table, VARCHAR
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)

    parent = relationship('Parent', back_populates='child')


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


class Demo(Base):
    __tablename__ = 'demo'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    password = Column(VARCHAR(255))


class Left(Base):
    __tablename__ = 'left'

    id = Column(Integer, primary_key=True)

    right = relationship('Right', secondary='association', back_populates='left')


class Pets(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    age = Column(Integer)
    type = Column(VARCHAR(30))


class Right(Base):
    __tablename__ = 'right'

    id = Column(Integer, primary_key=True)

    left = relationship('Left', secondary='association', back_populates='right')


class Table1(Base):
    __tablename__ = 'table1'

    id = Column(Integer, primary_key=True)

    table2 = relationship('Table2', back_populates='parent')


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    password = Column(VARCHAR(255))


t_association = Table(
    'association', metadata,
    Column('left_id', ForeignKey('left.id')),
    Column('right_id', ForeignKey('right.id'))
)


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    custid = Column(ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)

    customers = relationship('Customers', back_populates='invoices')


class Parent(Base):
    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)
    child_id = Column(ForeignKey('child.id'))

    child = relationship('Child', back_populates='parent')


class Table2(Base):
    __tablename__ = 'table2'

    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('table1.id'))

    parent = relationship('Table1', back_populates='table2')
