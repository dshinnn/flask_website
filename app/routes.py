from app import app
from flask import render_template, url_for, redirect
from app.form import PhonebookForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/phonebook', methods=['GET', 'POST'])
def phonebook():
    form = PhonebookForm()
    
    if form.validate_on_submit():
        print(form.name.data, form.phonenumber.data, form.email.data, form.address.data)
        with open('contacts.txt', 'a') as file:
            file.write(f'\nName: {form.name.data},  Phone Number: {form.phonenumber.data}, Email: {form.email.data}, Address: {form.address.data}')
        return redirect(url_for('index'))

    return render_template('phonebook.html', form=form)