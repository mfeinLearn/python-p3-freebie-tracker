#!/usr/bin/env python3

from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///freebies.db')
# engine = create_engine('sqlite:///freebie-tracker.db')

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
        Session = sessionmaker(bind=engine)
        session = Session()
        freebie = Freebie(item_name=item_name,value=value)
        freebie.dev = dev
        freebie.company = self
        session.add(freebie)
        session.commit()

        

    @classmethod
    def oldest_company(cls):
        # returns the Company instance with the earliest founding year.
        # ipdb.set_trace()
        Session = sessionmaker(bind=engine)
        session = Session()
        old_company = session.query(Company).all()[0]
        return old_company




        



## far right
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    companies = relationship('Company', secondary=company_dev, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Dev {self.name}>' # - delete this next time!!
        # return f'<Dev name={self.name}>' - use this next time!!

    def received_one(self,item_name):
        # Dev.received_one(item_name) accepts an item_name (string) and returns True if any of the freebies associated with the dev has that item_name, otherwise returns False.
        for d in self.freebies:
            if d.item_name == item_name:
                print('''

                    TRUEEEEEE
                
                ''')
                return True
        return False


    def give_away(self,dev, freebie):
        ###
        ###
        #-- broken need to fix!!!
        ###
        ###
        # Dev.give_away(dev, freebie) accepts a Dev instance and a Freebie instance, changes the freebie's dev to be the given dev; your code should only make the change if the freebie belongs to the dev who's giving it away
        Session = sessionmaker(bind=engine)
        session = Session()
        # # dev = self
        #freebie = session.query(Freebie).filter_by(dev_id=dev.id).first()
        print('''
        
        
        
        ******** HEY IM HERE!!!!!!!!!!!!!!!!!! ********


        
        
        ''')
        print(freebie)

        session.add(dev)
        session.commit()

        dev_just_added = session.query(Dev).order_by(Dev.id.desc()).first()

        freebie.dev_id = dev_just_added.id 
        session.commit()



      
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