from flask import flash, request, render_template, redirect, url_for, Blueprint, request
from flask_login import login_required, logout_user, login_user, user_logged_in, current_user

from inventory_app.app import db, check_admin
from inventory_app.app import bcrypt

from inventory_app.account.models import User, User_Role

account = Blueprint('account', __name__, template_folder="templates", static_folder="static")

# only for administrators
@account.route('/manageUsers', methods=['GET'])
@login_required
def manage_users():
    # render all users

    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "warning")
        return redirect(url_for('core.index'))

    users = User.query.all()
    roles = User_Role.query.all()
    return render_template('account/administrar-usuarios.html', users=users, roles=roles)

@account.route('/registerUser', methods=['GET', 'POST'])
@login_required
def register_user():

    if current_user.user_role.user_role != "admin":
        flash("No estás autorizado para crear un nuevo usuario", "warning")
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
            flash('Las contraseñas no coinciden', "error")
            return redirect(url_for('account.register_user')) 

        hashed_password = bcrypt.generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password, user_role_id=user_role_id)

        # add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # redirect to the main page
        flash('Usuario añadido satisfactoriamente', "success")
        return redirect(url_for('core.index'))

    return render_template('account/register_user.html')

@account.route('/manageUsers/deleteUser', methods=['POST'])
@login_required
def delete_user():
    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "warning")
        return redirect(url_for('core.index'))

    user_id = request.form['user_id']

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('account.manage_users'))

@account.route('/manageUsers/editUser', methods=['POST'])
@login_required
def edit_user():
    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "warning")
        return redirect(url_for('core.index'))

    user_id = request.form['user_id']
    user_role_id = request.form['role']
    username = request.form['username']
    email = request.form['email']

    user = User.query.get(user_id)
    user.user_role_id = user_role_id
    user.username = username
    user.email = email
    db.session.commit()

    flash("Usuario editado exitosamente", "success")
    return redirect(url_for('account.manage_users'))


@account.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        print(current_user)
        # redirect to the main page
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        # grab the user information
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            print(user)
            login_user(user)

            flash('Inicio de sesión exitoso', "success")
            return redirect(url_for('core.index'))

        flash('Inicio de sesión fallido. Por favor, revisa tus credenciales', "error")
        return redirect(url_for('account.login'))

    return render_template('account/login.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()

    flash("Se ha cerrado la sesión", "success")
    return redirect(url_for('account.login'))

@account.route('/profile')
@login_required
def profile():
    print(current_user)

    admin = False
    if check_admin(current_user):
        admin = True

    return render_template('account/profile.html', admin=admin)
