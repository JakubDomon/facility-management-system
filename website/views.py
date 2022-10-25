from random import random
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import query
from flask_login import login_required, current_user
from website.access_control import admin_access
from website.models import User, db
from time import time
from flask import jsonify

## UTWORZENIE BLUEPRINTA
views = Blueprint('views', __name__)

## URL ROUTING
@views.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('auth.login'))

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
    if request.method == 'POST':
        if request.json['data'] == "send":
            randomize = random()*100
            response = {
                "status": "200",
                "randomNumber": randomize,
                "daysChart": {
                    "day1": "Poniedziałek",
                    "day2": "Wtorek"
                },
                "dataChart": {
                    "data1": randomize,
                    "data2": randomize*1.5
                }
            }
            return response
    return render_template('dashboard.html', user=current_user)

@views.route('/success_login', methods=['GET', 'POST'])
@login_required
def success_login():
    return render_template('success_login.html', user=current_user)

@views.route('/success_create', methods=['GET', 'POST'])
@login_required
@admin_access
def success_create():
    return render_template('success_create.html', user=current_user)

@views.route('/delete', methods=['GET', 'POST'])
@login_required
@admin_access
def delete():
    if request.method == 'POST':
        user_id = request.json['ID']
        User.query.filter(User.id == user_id).delete()
        db.session.commit()
        response = {
            "data": "200"
        }
        return response

    users_ls = User.query.order_by(User.id).all()
    return render_template('delete.html', user=current_user, users=users_ls)
