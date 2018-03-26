'''Flask App'''
from iot import create_app
from config import Config

if __name__ == '__main__':
    app = create_app(Config)
    app.run(threaded=True) #Fix Slow Requests on Local Flask Server

