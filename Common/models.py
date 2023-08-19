from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    year_joined = Column(Integer, nullable=False)
