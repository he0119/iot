'''Flask App'''
import click

from config import Config
from iot import create_app, db, socketio
from iot.models.user import User

app = create_app(Config)


@app.cli.command()
def createaccount():
    '''create a new account'''
    with app.app_context():
        if db.session.query(User).filter(User.username == app.config.get('ADMIN_USERNAME')).first():
            click.echo('You have already created a user')
        else:
            if db.session.query(User).filter(User.email == app.config.get('ADMIN_EMAIL')).first():
                click.echo('This Email has been used, please change')
            else:
                new_user = User(username=app.config.get('ADMIN_USERNAME'),
                                email=app.config.get('ADMIN_EMAIL'))
                new_user.set_password(app.config.get('ADMIN_PASSWORD'))
                db.session.add(new_user)
                db.session.commit()
                click.echo('Account Created')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', log_output=True)
