from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    stocks_id = Column(String, index=True)
    datetime = Column(String, index=True)
    symbol = Column(String, index=True)
    shortName = Column(String, index=True)
    price = Column(Float)
    currency = Column(String)
    source = Column(String)


# class Company(Base):
#     __tablename__ = "companies"

#     id = Column(Integer, primary_key=True, index=True)
#     symbol = Column(String, index=True)
#     shortName = Column(String, index=True)
#     price = Column(Float)
#     currency = Column(String)