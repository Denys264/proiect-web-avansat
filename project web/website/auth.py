from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json

auth= Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':    
        username=request.form.get("username")
        password=request.form.get("password")
        user= User.query.filter_by(username=username).first()
        if(username=='admin'and password=='informatica'):
            return redirect(url_for('views.admin'))
        elif  user:
            print("Utilizatorul exista")
            if  check_password_hash(user.password, password):
                flash("Logged in")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print("parola incorecta")
                flash('password is incorect!', category='error')
               
        else:
            print("username gresit")
            flash('Email does not exist!', category='error')
    return render_template("Sign in.html")

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("pass")

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        if user_exists:
            print("Usernameul deja exista")
            flash('Username already exist!', category='error')
        elif email_exists:
            print("Emailul deja exista")
            flash('Email already in using!', category='error')
        elif len(username) <2:
            print("Usernameul este prea scurt")
            flash('Username is too short!', category='error')
        elif len(password)<6:
            print("Parola prea scurta")
            flash('Password is too short!', category='error')
        else:

            new_User=User(email=email, username=username,password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_User)
            db.session.commit()
            login_user(new_User, remember=True)
            flash('User created')
            print("utilizatorul cu username" + username + "si parola " + password + "a fost creat cu succes")
            return redirect(url_for('views.home'))
    return render_template("Sign up.html")



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))