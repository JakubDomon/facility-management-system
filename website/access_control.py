from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for
from flask_login import current_user

# DETECTING CURRENT USER
usr = current_user

# ROLE BASE ACCESS CONTROL
# Arguments:
# - routing function
# Output:
# - pass to routing function
# - redirect to dashboard
def admin_access(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if usr.role.name != 'admin':
            return redirect(url_for('views.dashboard'))   
        return function(*args, **kwargs)
    return wrapper

