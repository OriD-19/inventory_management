from flask import flash, request, render_template, redirect, url_for, Blueprint, request
from flask_login import login_required, logout_user, login_user, user_logged_in, current_user

from inventory_app.app import db, check_admin
from inventory_app.app import bcrypt

from inventory_app.account.models import User

account = Blueprint('account', __name__, template_folder="templates")

# only for administrators
@account.route('/manageUsers', methods=['GET'])
@login_required
def all_users():
    # render all users

    if not check_admin(current_user):
        flash("You are not authorized to view this page.")
        return redirect(url_for('core.index'))

    users = User.query.all()
    return render_template('account/all_users.html', users=users)


@account.route('/registerUser', methods=['GET', 'POST'])
@login_required
def register_user():

    if current_user.user_role.user_role != "admin":
        flash("You cannot create a new user.")
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        print(current_user.user_role)
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
        return redirect(url_for('core.index'))

    return render_template('account/register_user.html')

@account.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        # redirect to the main page
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        # grab the user information
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        print("user", user)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('core.index'))

        flash('Login failed. Please check your username and password.')
        return redirect(url_for('account.login'))

    return render_template('account/login.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('account.login'))

