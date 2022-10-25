from website import create_app, db
from website.models import Role, User
from werkzeug.security import generate_password_hash

# UTWORZENIE INSTANCJI
app = create_app()

@app.before_first_request
def before_first_request():
    if not (db.session.query(db.exists().where(Role.name == 'admin')).scalar() and db.session.query(db.exists().where(Role.name == 'user')).scalar()):
        newRole1 = Role(name = "admin")
        newRole2 = Role(name = "user")
        firstAdminUser = User(empNb=1234567, empName = 'Admin Admin', password= generate_password_hash("firstAdmin"),role_id = 1)
        thingsToAdd = [newRole1, newRole2, firstAdminUser]
        db.session.add_all(thingsToAdd)
        db.session.commit()

# START APKI
if __name__ == '__main__':
    app.run(debug=True)