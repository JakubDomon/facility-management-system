from django.shortcuts import render
from flask import Blueprint, render_template, request

## UTWORZENIE BLUEPRINTA
views = Blueprint('views', __name__)

## URL ROUTING
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    data = request.form
    print(data)
    return render_template('contact.html')


@views.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error_submit.html')

@views.route('/manager', methods=['GET', 'POST'])
def manage():
    return render_template('manager.html')