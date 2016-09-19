from flask import Flask, Response, render_template, request, redirect, url_for, flash, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Expires, User
import pandas as pd
import csv
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sql import db, User

app = Flask(__name__)
app.debug = True
app.config['SERVER_NAME'] = 'localserver:5000'
app.config['SECRET_KEY']= 'something_secret'

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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

@login_manager.user_loader
def user_loader(user_id):
    print User.query.get(user_id).is_authenticated()
    return User.query.get(user_id)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
	print "Posted"
	email = request.form['email']
	password = request.form['password']
	print email,password
        user = User.query.get(email)
        if user:
	    print user.password
            #if bcrypt.check_password_hash(user.password, password):
            if user.password == password:
	        user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
		print "Authenticated."
                return redirect(url_for('sub_index',api='api'))
    return Response('''
        <form action="" method="post">
            <p><input type=text name=email>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p> Login Failed </p>')

@app.route('/', subdomain="<api>", methods=['GET'])
@login_required
def sub_index(api):
    print "Subbing"
    return "hello {}".format(api)

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
                session.merge(entry)
                session.commit()
            if '_num_good' in k:
	        ml_id = k.split('_')[0]
	        entry = session.query(Expires).filter_by(ml=ml_id).first()
		entry.num_good = request.form[k]
                session.merge(entry)
                session.commit()
	return redirect(url_for('date_page', date=date, style=style))
    
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
