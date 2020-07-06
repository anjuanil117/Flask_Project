import os
import cv2
from datetime import datetime
from flaskblog import app,db,bcrypt
from flask import Flask,render_template,flash,redirect,url_for,logging,request,Response,flash
from flaskblog.forms import RegistrationForm,LoginForm 
from flaskblog.models import User,Post
from flask_login import login_user
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import scoped_session,sessionmaker
# from passlib.hash import sha256_crypt
# from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename



# UPLOAD_FOLDER = 'flaskblog/uploads'







posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/home")  
def home():
    return render_template("home.html")
@app.route("/about")    
def about():
    return render_template("about.html",title='about')

@app.route("/index") 
def index():
    return render_template("upload.html")
    
    
@app.route("/Register",methods=["GET","POST"]) 
def Register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Login'))
    return render_template('register.html', title='Register', form=form)
    
            
    
    
@app.route("/Login", methods=['GET', 'POST'])
def Login():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('Login.html', title='Login', form=form)
    


@app.route('/upload',methods=["POST"])
def upload():
    
    if request.method == 'POST':
        file1= request.files['photo']
        basedir = os.path.abspath(os.path.dirname(__file__))
        file1.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], file1.filename))
        image=cv2.imread('uploads/'+file1.filename)  
        
        print(file1.filename)
        
        return render_template("complete.html")



