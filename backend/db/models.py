from sqlalchemy import Column, Integer, String, Float, Date, BigInteger, ForeignKey, Boolean, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(32), unique=True, nullable=False)
    name = Column(String)
    sector = Column(String)
    prices = relationship('DailyPrice', back_populates='company')

class UploadedFile(Base):
    __tablename__ = 'uploaded_files'
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    upload_date = Column(TIMESTAMP)
    md5 = Column(String(64), unique=True)
    rows_extracted = Column(Integer)
    success = Column(Boolean)
    prices = relationship('DailyPrice', back_populates='source_file')

class DailyPrice(Base):
    __tablename__ = 'daily_prices'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    date = Column(Date, nullable=False)
    pclose = Column(Numeric)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    change = Column(Numeric)
    deals = Column(Integer)
    volume = Column(BigInteger)
    value = Column(Numeric)
    vwap = Column(Numeric)
    source_file_id = Column(Integer, ForeignKey('uploaded_files.id'))
    company = relationship('Company', back_populates='prices')
    source_file = relationship('UploadedFile', back_populates='prices')
