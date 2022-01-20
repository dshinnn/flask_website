import json
from app import app
from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.form import PhonebookForm, RegisterForm, LoginForm
from app.models import User, Phonebook

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/phonebook', methods=['GET', 'POST'])
@login_required
def phonebook():
    form = PhonebookForm()
    
    if form.validate_on_submit():
        name = form.name.data
        phonenumber = form.phonenumber.data
        email = form.email.data
        address = form.address.data

        Phonebook(name=name, phonenumber=phonenumber, email=email, address=address)
        return redirect(url_for('index'))

    return render_template('phonebook.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        
        if not user:
            User(username=username, password=password)
            return render_template('index.html')
        else:
            print('Username already exists')
        return render_template('register.html')
        
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Checks if username and password are not null
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Checks if the username exists and if the password matches
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            print('Username does not exist')
            return redirect(url_for('login'))

        # If username exists and the password match, login user
        login_user(user)
        print('Sucessfully logged in')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    print('Successfully logged out')
    return redirect(url_for('index'))