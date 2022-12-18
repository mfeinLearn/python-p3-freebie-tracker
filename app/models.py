#!/usr/bin/env python3

from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///freebie-tracker.db')

Base = declarative_base()


company_dev = Table(
    'company_devs',
    Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('company_id', ForeignKey('companies.id')),
    Column('dev_id', ForeignKey('devs.id')),
    extend_existing=True,
)


## far left 

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    devs = relationship('Dev', secondary=company_dev, back_populates='companies')
    freebies = relationship('Freebie', backref=backref('company'))

    def __repr__(self):
        return f'<Company name={self.name}, ' + \
            f'founding_year={self.founding_year}>'

    def give_freebie(self ,dev, item_name, value):
        # creates a new Freebie instance associated with this company and the given dev
        freebie1 = Freebie(item_name, value)
        freebie1.dev = dev
        freebie1.company = self
        return freebie1

    @classmethod
    def oldest_company(cls):
        pass
        # returns the Company instance with the earliest founding year.

        



## far right
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    companies = relationship('Company', secondary=company_dev, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'))

    def __repr__(self):
        return f'<Dev {self.name}>' # - delete this next time!!
        # return f'<Dev name={self.name}>' - use this next time!!

    def received_one(self,item_name):
        pass

    def give_away(self,dev, freebie):
        pass


      
## join table
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
  
    item_name= Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


    def __repr__(self):
        return f'<Freebie item_name={self.item_name}, ' + \
            f'value={self.value}, ' + \
            f'company_id={self.company_id}, ' + \
            f'dev_id={self.dev_id})>'
    
    def print_details(self):
        return(f'{self.dev.name} owns a {self.item_name} from {self.company.name}')