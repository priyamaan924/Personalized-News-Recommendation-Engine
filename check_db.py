
from app import create_app, db
from app.models import User
from getpass import getpass

app = create_app()

with app.app_context():

    print("\n===== NEWSAI DATABASE CHECK =====")

    print("Database location:", db.engine.url.database)

    print("Total registered users:", User.query.count())

    email = input("\nEnter your registered email: ").strip().lower()

    user = User.query.filter_by(email=email).first()

    if user:
        print("\nSUCCESS: User found in database!")

        password = getpass("Enter your password: ")

        if user.check_password(password):
            print("SUCCESS: Password matches!")
        else:
            print("ERROR: Password does not match.")

    else:
        print("\nERROR: User not found in database.")
