import sys
from sqlalchemy import Column, ForeignKey, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Expires(Base):
   	__tablename__ = 'expires'
	
	date_added = Column(Date)

    	ml = Column(String(32), nullable=False, primary_key=True)
	status = Column(String(32))
	current_price = Column(String(32))
	list_price = Column(String(32))
	address = Column(String(32))
	street_name = Column(String(32))
	street_num  = Column(String(32))
	city = Column(String(32))
	zip = Column(String(32))
	dom = Column(String(32))

	own_first = Column(String(32))
	own_last = Column(String(32))
	own_mid = Column(String(32))

	own_alt_first = Column(String(32))
	own_alt_last = Column(String(32))
	own_alt_mid = Column(String(32))

	own_add_same_as_prop = Column(String(32))
	own_city_st = Column(String(32))
	own_address = Column(String(32))
	own_zip = Column(String(32))

	parcel_code = Column(String(64))
	
	agent_phone = Column(String(32))
	agent_email = Column(String(32))
	agent_name = Column(String(32))
	agent_mls = Column(String(32))

	office_mls = Column(String(32))
	office_name = Column(String(64))
	office_phone = Column(String(32))

	list_date = Column(String(32))
	phone = Column(String(32))

	# Input Information
	num_good = Column(String(32))
	list_status = Column(String(32))
	comments = Column(String(64))

engine = create_engine('sqlite:///expires.db')
Base.metadata.create_all(engine)
