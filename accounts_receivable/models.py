from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import TEXT, INTEGER, Column, REAL, ForeignKey

base = declarative_base()
    
class Client(base):
    __tablename__ = 'client_list'
    
    client_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    phone = Column(TEXT)
    address_1 = Column(TEXT)
    address_2 = Column(TEXT)
    city = Column(TEXT)
    state = Column(TEXT)
    zipcode = Column(TEXT)
    email = Column(TEXT)
    invoice = relationship('Invoice', back_populates='client_info', lazy='joined')
    
class Invoice(base):
    __tablename__ = 'invoice'
    
    invoice_id = Column(INTEGER, primary_key=True)
    client_id = Column(INTEGER, ForeignKey(Client.client_id))
    invoice_date = Column(TEXT)
    pay_date = Column(TEXT)
    line_items = Column(TEXT)
    total = Column(REAL)
    status = Column(TEXT)
    url = Column(TEXT)
    payment_id = Column(TEXT)
    client_info = relationship('Client', back_populates='invoice', lazy='joined')
