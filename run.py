'''Flask App'''
import getpass

import click

from config import Config
from iot import create_app, db, socketio
from iot.models.user import User

app = create_app(Config)


@app.cli.command()
def devicedatatosql():
    '''device data to sql format'''
    with app.app_context():
        username = input('Please enter your username: ')
        with open('devicedata.sql', 'w') as f:
            devicedata = db.session.query(User).filter(
                User.username == username).first().devices.first().data.all()
            i = 0
            end = len(devicedata)
            f.write('INSERT INTO `devicedata` VALUES ')
            for data in devicedata:
                i += 1
                f.write(
                    f"({data.id},'{data.time.isoformat().replace('T', ' ')}','{data.data}',{data.device_id})")

                if i < end:
                    f.write(',')
                else:
                    f.write(';')


@app.cli.command()
def createaccount():
    '''create a new account'''
    username = input('Please enter your username: ')
    while True:
        password = getpass.getpass('Please enter your password: ')
        password2 = getpass.getpass('Please enter your password again: ')
        if password == password2:
            break
        print("Password mismatch, please try again")

    email = input('Please enter your email: ')
    with app.app_context():
        if db.session.query(User).filter(User.username == username).first():
            click.echo('You have already created a user')
        else:
            if db.session.query(User).filter(User.email == email).first():
                click.echo('This Email has been used, please change')
            else:
                new_user = User(username=username,
                                email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                click.echo('Account Created')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', log_output=True)
