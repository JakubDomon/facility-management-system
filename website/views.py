from random import random
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.access_control import admin_access
from website.models import User, db, Machine, OPCUA
from website import OWM

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

    OWM.query_collection()
    return render_template('contact.html', user=current_user, weather = OWM)

@views.route('/error', methods=['GET', 'POST'])
@login_required
def error():

    OWM.query_collection()
    return render_template('error_submit.html', user=current_user, weather = OWM)

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

    OWM.query_collection()
    return render_template('dashboard.html', user=current_user, weather = OWM)

@views.route('/success_login', methods=['GET'])
@login_required
def success_login():
    return render_template('success_login.html', user=current_user)

@views.route('/success_create', methods=['GET'])
@login_required
@admin_access
def success_create():
    return render_template('success_create.html', user=current_user)

@views.route('/success_add', methods=['GET'])
@login_required
@admin_access
def success_add():
    return render_template('success_add.html', user=current_user)

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
    OWM.query_collection()
    return render_template('delete.html', user=current_user, users=users_ls, weather = OWM)

@views.route('/delete_machine', methods=['GET', 'POST'])
@login_required
@admin_access
def delete_machine():

    if request.method == 'POST':
        machine_id = request.json['ID']
        machineToDelete = Machine.query.filter(Machine.id == machine_id).first()
        db.session.delete(machineToDelete)
        db.session.commit()
        response = {
            "data": "200"
        }
        return response

    machines_ls = Machine.query.order_by(Machine.id).all()
    OWM.query_collection()
    return render_template('delete_machine.html', user=current_user, machines=machines_ls, weather = OWM)

@views.route('/add_machine', methods=['GET', 'POST'])
@login_required
@admin_access
def add_machine():
    if request.method == 'POST':
        machine_name = request.form.get('machine_name')
        machine_date = request.form.get('machine_date')
        machine_endpoint = request.form.get('machine_endpoint')
        machine_node = request.form.get('machine_node')

        opc = OPCUA.query.filter_by(endpoint = machine_endpoint).first()
        
        if opc:
            flash('Stanowisko o podanych danych już istnieje')
            return render_template('add_machine.html', user=current_user)

        newMachine = Machine(name = machine_name, dateOfProduction = machine_date, addedBy = current_user.empName)
        db.session.add(newMachine)
        db.session.commit()

        machine = Machine.query.filter_by(name = machine_name).first()

        newOPC = OPCUA(endpoint = machine_endpoint, nodes = machine_node, machine_id = machine.id)

        db.session.add(newOPC)
        db.session.commit()

        return redirect(url_for('views.success_add'))

    OWM.query_collection()
    return render_template('add_machine.html', user=current_user, weather = OWM)