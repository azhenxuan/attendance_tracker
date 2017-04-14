from getpass import getpass
import sys

from flask import current_app
from flask_bcrypt import Bcrypt
from attendance_updater import create_app
from attendance_updater.models import User, db

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print('A user already exists! Create another? (yes/no):')
            create = raw_input()
            if create == 'no':
                return

        print('Enter email address: ')
        email = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')

if __name__ == '__main__':
    sys.exit(main())
