from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
## UTWORZENIE BLUEPRINTA
views = Blueprint('views', __name__)

## URL ROUTING
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    data = request.form
    print(data)
    return render_template('contact.html', user=current_user)

@views.route('/error', methods=['GET', 'POST'])
@login_required
def error():
    return render_template('error_submit.html', user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/success_login', methods=['GET', 'POST'])
@login_required
def success_login():
    return render_template('success_login.html', user=current_user)

@views.route('/success_create', methods=['GET', 'POST'])
@login_required
def success_create():
    return render_template('success_create.html', user=current_user)