from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.wrappers import Request
import flask_login
from sqlalchemy.sql.expression import false
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route('login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('Password')
        user =  User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully Loged in!')
                login_user(user, remember= True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password','error')
        else:
            flash('Email not signed up, sign up','error')
            return redirect(url_for('auth.signup'))
        
    return render_template('login.html', User= current_user)

@auth.route('logout')
@login_required
def logout():
    flash("Logged out Successfully")
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        p1 = request.form.get('Password1')
        p2 = request.form.get('Password2')
        if p1 != p2:
            flash("Passwords do not match", 'error')
        elif not re.fullmatch(regex_email,email):
            flash("Enter Valid Email",'error')
        elif len(firstname) <= 1:
            flash("Enter Valid Name", 'error')
        else:
            ex_user = User.query.filter_by(email = email).first()
            if ex_user:
                flash("User already exists, login", "error")
                return redirect(url_for('auth.login'))
            user = User(email = email, first_name = firstname, password = generate_password_hash(p1, "sha256"))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully")
            login_user(user, remember= True)
            return redirect(url_for('views.home'))
            

    return render_template('Signup.html', User= current_user)
