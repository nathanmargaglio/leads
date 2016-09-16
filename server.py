from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Expires
import pandas as pd
import csv

app = Flask(__name__)
engine = create_engine('sqlite:///expires.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def get_cities():
    f = open('cities.txt')
    list =  f.read().split(',')
    f.close()
    return list

cities =  get_cities()

@app.route("/",methods=['GET','POST'])
def index():
    data = session.query(Expires.date_added).distinct()
    if request.method == 'POST':
	date  = request.form.get('date_option')
    	style = request.form.get('style')
	print date,style
        return redirect(url_for('date_page',date=date,style=style))
    data = sorted(data)[::-1]
    return render_template('index.html', data=data)

@app.route("/expires", methods=['GET','POST'])
def date_page():
    date  = request.args.get('date')
    style = request.args.get('style')
    print "Style:",style,style=='limited'
    #date = pd.to_datetime(date).date()
    if request.method == 'GET':
        if style=="limited":
	    data = session.query(Expires).filter(Expires.date_added == date, Expires.phone != None, Expires.city.in_(cities))
        else:
            data = session.query(Expires).filter(Expires.date_added == date, Expires.phone != None)
	return render_template('tables.html',data=data)
    else:
	for k in request.form:
            if '_comment' in k:
       		ml_id = k.split('_')[0]
		entry = session.query(Expires).filter_by(ml=ml_id).first()
                entry.comments = request.form[k]
            if '_num_good' in k:
	        ml_id = k.split('_')[0]
	        entry = session.query(Expires).filter_by(ml=ml_id).first()
		entry.num_good = request.form[k]
	return redirect(url_for('date_page', date=date, style=style))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
