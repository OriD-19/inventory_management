from flask import flash, request, render_template, redirect, url_for, Blueprint, request
from flask_login import login_required, logout_user, login_user

from inventory_app.app import db
from inventory_app.app import bcrypt

from inventory_app.account.models import User

account = Blueprint('account', __name__, template_folder="templates")

"""
There is no signup form exposed to the public
This endpoint is going to be avaiable ONLY to the admin user
"""
@account.route('/registerUser', methods=['GET', 'POST'])
def register_user():

    if request.method == 'POST':
        # grab the user information
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_role_id = request.form['role']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('account.register_user')) 

        hashed_password = bcrypt.generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password, user_role_id=user_role_id)

        # add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # redirect to the main page
        flash('User added successfully!')
        return redirect(url_for('categories.index'))

    return render_template('account/register_user.html')

@account.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # grab the user information
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('categories.index'))

        flash('Login failed. Please check your username and password.')
        return redirect(url_for('account.login'))

    return render_template('account/login.html')

@account.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('account.login'))

