import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Expires
import os

engine = create_engine('sqlite:///expires.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def database_parser(name):
	date = name.replace('_','/')
	date_added = pd.to_datetime(date).date()
	print date_added
    	for row in pd.read_csv('data/'+name+'/results.csv').iterrows():
		r = row[1]
		entry = Expires(date_added = date_added)
		entry.ml = r['ML #']
		entry.status = r['St']
		entry.current_price = r['Current Price']
		entry.list_price = r['List Price']
		entry.address = r['Address']
		entry.street_name = r['Street Name']
		entry.street_num = r['Street Number']
		entry.city = r['City']
		entry.zip = r['Zip Code_x']
		entry.dom = r['DOM']
		
		entry.own_first = r['Owner 1 First Name']
		entry.own_last = r['Owner 1 Last Name']
		entry.own_mid = r['Owner 1 Middle Initial']
		
		entry.own_alt_first = r['Owner 2 First Name']
		entry.own_alt_last = r['Owner 2 Last Name']
		entry.own_alt_mid = r['Owner 2 Middle Initial']

		entry.own_add_same_as_prop = r['Owner Address Same as Property YN']
		entry.own_city_st = r['Owner City State']
		entry.own_address = r['Owner Street Num Street Name']
		entry.zip = r['Owner Zip Code']

		entry.parcel_code = r['Parcel Number']
		entry.agent_phone = r['List Agent Direct Work Phone']
		entry.agent_email = r['List Agent Email']
		entry.agent_name = r['List Agent Full Name']
		entry.agent_mls = r['List Agent MLSID']

		entry.office_mls = r['List Office MLSID']
		entry.office_name = r['List Office Name']
		entry.office_phone = r['List Office Phone']

		entry.list_date = r['List Date']
		entry.phone = r['Phone']

		try:
			session.add(entry)
			session.commit()
		except Exception,e:
			session.rollback()
			print str(e)
