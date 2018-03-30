'''Flask App'''
import sys

from config import Config
from iot import create_app, db
from iot.models.user import User

app = create_app(Config)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(threaded=True) #Fix Slow Requests on Local Flask Server
    else:
        with app.app_context():
            if db.session.query(User).filter(User.username == Config.ADMIN_USERNAME).first():
                print('You have already created a user')
            else:
                new_user = User(username=Config.ADMIN_USERNAME, email=Config.ADMIN_EMAIL)
                new_user.set_password(Config.ADMIN_PASSWORD)
                db.session.add(new_user)
                db.session.commit()
                print('Account Created')
