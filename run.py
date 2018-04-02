'''Flask App'''
import click

from config import Config
from iot import create_app, db
from iot.models.user import User

app = create_app(Config)

@app.cli.command()
def createaccount():
    '''create a new account'''
    with app.app_context():
        if db.session.query(User).filter(User.username == Config.ADMIN_USERNAME).first():
            click.echo('You have already created a user')
        else:
            if  db.session.query(User).filter(User.email == Config.ADMIN_EMAIL).first():
                click.echo('This Email has been used, please change')
            else:
                new_user = User(username=Config.ADMIN_USERNAME, email=Config.ADMIN_EMAIL)
                new_user.set_password(Config.ADMIN_PASSWORD)
                db.session.add(new_user)
                db.session.commit()
                click.echo('Account Created')

if __name__ == '__main__':
    app.run(threaded=True) #Fix Slow Requests on Local Flask Server
