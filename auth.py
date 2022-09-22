#for authentication operations
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models import User
from app import db

auth = Blueprint('auth', __name__)

#route for login
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    #code to login
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    #check if user exists and check password passed if it compares to the saved hash
    if not user or not check_password_hash(user.password, password):
        flash('Username or Password incorrect')
        return redirect(url_for('auth.login'))
    
    #if it checks and correct details have been passed
    login_user(user, remember=remember)
    return redirect(url_for('main.home'))

#route for adding a user
@auth.route('/addUser')
def addUser():
    return render_template('addUser.html')

#function to hold POST form data
@auth.route('/addUser', methods=['POST'])
def addUser_post():

    #validate the user
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() #if it returns a user then email is already registered

    if user:
        flash('Email address already registered')
        return redirect(url_for('auth.addUser'))

    #create new user
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256', salt_length=16))

    #add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('New user successfully created. You may login using the new credentials')
    return redirect(url_for('auth.addUser'))

#route for logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))