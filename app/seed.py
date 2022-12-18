#!/usr/bin/env python3

# Script goes here!
# from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company
from models import Dev
from models import Freebie


# fake = Faker()

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

    # company

    ibm = Company(name="IBM", founding_year=1911)
    fi_school = Company(name="Flatiron School ", founding_year=2012)
    # dev 

    malcome = Dev(name="Malcome")
    nick = Dev(name="Nick")

    # Freebie
    book = Freebie(item_name="Book", value=12, company_id=1, dev_id=1)
    planer = Freebie(item_name="Planer", value=13, company_id=2, dev_id=1)

    # got = Freebie(item_name="Game of Thrones", value=6, company_id=1, dev_id=1)

    # pen = Freebie(item_name="Pen", value=5, company_id=1, dev_id=1)

    session.bulk_save_objects([ibm,fi_school,malcome,nick,book,planer ])

    session.commit()
