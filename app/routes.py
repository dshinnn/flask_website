import json
from app import app
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.form import PhonebookForm, RegisterForm, LoginForm, EditPhonebookForm
from app.models import User, Phonebook

@app.route('/')
def index():
    phonebook = Phonebook.query.all()
    return render_template('index.html', phonebook=phonebook)

# Registers new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # Checks if user inputs are valid
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Queries for inputted username 
        user = User.query.filter_by(username=username).first()
        
        # Checks if the inputted username exists already, if not creates new user
        if not user:
            User(username=username, password=password)
            flash(f'User { username } has successfully been created!', 'success')
            return redirect(url_for('login'))

        else:
            flash(f'User { username } already exists', 'warning')
        return redirect(url_for('register'))
        
    return render_template('register.html', form=form)

# Logs in user
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
            flash(f'{ username } or password is invalid', 'danger')
            return redirect(url_for('login'))

        # If username exists and the password match, login user
        login_user(user)
        flash(f'Logged in as: { username }', 'secondary')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

# Logs out user
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('index'))

# CREATE
@app.route('/phonebook', methods=['GET', 'POST'])
@login_required
def phonebook():
    form = PhonebookForm()

    if form.validate_on_submit():
        name = form.name.data
        phonenumber = form.phonenumber.data
        email = form.email.data
        address = form.address.data

        phonebook = Phonebook(name=name, phonenumber=phonenumber, email=email, address=address, user_id=current_user.id)
        
        flash(f'{ name } has been successfully added to your contacts!', 'success')
        return redirect(url_for('index'), phonebook=phonebook)

    return render_template('phonebook.html', form=form)

# Loads contact page when the "More Info" button is clicked
@app.route('/phonebook/<int:contact_id>')
def contact_info(contact_id):
    contact = Phonebook.query.get_or_404(contact_id)
    return render_template('contact.html', contact=contact)

# UPDATE
@app.route('/phonebook/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit(contact_id):
    form = EditPhonebookForm()
    form.user_id=current_user.id
    contact = Phonebook.query.get_or_404(contact_id)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.phonenumber = form.phonenumber.data
        contact.email = form.email.data
        contact.address = form.address.data
        contact.save_contact()
        flash(f"{contact.name} has been updated", "primary")
        return redirect(url_for('contact_info', contact_id=contact.id))
    return render_template('edit_phonebook.html', form=form, contact=contact)
