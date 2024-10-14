from flask import Blueprint, render_template, request, redirect, url_for
from inventory_app.app import db
from inventory_app.trial.models import Trial

trial = Blueprint('trial', __name__, template_folder='templates')

@trial.route('/')
def index():
    trials = Trial.query.all()

    return render_template('trial/index.html', trials=trials)

@trial.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('trial/create.html')
    elif request.method == 'POST':
        category = request.form.get('name')

        trial = Trial(category=category)
        db.session.add(trial)
        db.session.commit()

        return redirect(url_for('trial.index'))