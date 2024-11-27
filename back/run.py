from back import db, app, bcrypt
from back.model import Role, User
from flask_security import Security, SQLAlchemyUserDatastore
from flask import request, jsonify
from flask_cors import cross_origin
from sqlalchemy import func

from back import workers

celery = workers.celery

celery.Task = workers.ContextTask
app.app_context().push()


@app.route("/usersignup", methods=["GET", "POST"])
@cross_origin()
def user_signup():
    if request.method == "POST":
        # Extract data from the request
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        userType = request.form.get("userType")

        existing_username = User.query.filter(
            func.lower(User.username) == func.lower(username)
        ).first()

        existing_email = User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first()
        if existing_username:
            return jsonify({"flash": "Username already exists"})
        elif existing_email:
            return jsonify({"flash": "Email already exists"})
        else:
            hash_password = bcrypt.generate_password_hash(password)

            # Create a new user (you should hash the password in a real application)
            user = user_datastore.create_user(
                username=username, email=email, password=hash_password
            )

            if userType == "user":
                user_role = Role.query.filter_by(name="user").first()
                user_datastore.add_role_to_user(user, user_role)
            else:
                manager_role = Role.query.filter_by(name="manager").first()
                user_datastore.add_role_to_user(user, manager_role)
            db.session.commit()

            # Add the user to the database
            db.session.add(user)
            db.session.commit()

            # login_user(user)
            # Return a success message to the client
            return jsonify({"success": "You signed up successfully"}), 201

    return jsonify({"message": "You reached signup endpoint"})


if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
        db.create_all()

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = Security(app, user_datastore)
        # Create the roles
        user_role = Role.query.filter_by(name="user").first()
        if user_role is None:
            user_role = Role(name="user")
            db.session.add(user_role)

        admin_role = Role.query.filter_by(name="admin").first()
        if admin_role is None:
            admin_role = Role(name="admin")
            db.session.add(admin_role)

        manager_role = Role.query.filter_by(name="manager").first()
        if manager_role is None:
            manager_role = Role(name="manager")
            db.session.add(manager_role)

        db.session.commit()

        # Create the admin user
        if db.session.query(User).count() == 0:
            admin = user_datastore.create_user(
                username="admin",
                email="admin@example.com",
                password=bcrypt.generate_password_hash("password"),
            )
            user_datastore.add_role_to_user(admin, admin_role)
            db.session.commit()

    # Run the application
    app.run(debug=True)
