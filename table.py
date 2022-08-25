from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine=None
#DB_URL = "oracle+://system:oracle@hostname:1521/localhost_XE"
DB_URL = "oracle+cx_oracle://system:oracle@localhost:1521/xe"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()
company_table = Table(
    "Company",
    metadata,
    Column('id', Integer),
    Column('name', String(30)),
    Column('department', String(30)))
metadata.create_all(engine)

ins = company_table.insert().values(id='6',name='ram', department='HR')
connection=engine.connect()
result = connection.execute(ins)


