# IOT
Simple try for home automation using Python, Flask, Angular, MQTT, Arduino

## Requirements
* Python 3.6.4
* Node.js 8.10.0

## Getting Started
1. Setup python environment
    ```
    virtualenv --no-site-packages venv
    source venv/bin/activite
    pip install -r requirements.txt
    ```
2. Setup angular environment
	
	```
    cd iot\angular
    npm install -g @angular/cli
	npm install
    ng build --prod
	```
3. Configuration
    
    1. Create a ```py.conf``` file in configuration folder
    ```
    [admin]
    username=
    password=
    email=

    [mqtt]
    id=test_server
    username=
    password=
    url=broker.shiftr.io
    port=8883
    ```
    2. Init database
    ```
    export FLASK_APP=hello.py(set FLASK_APP=hello.py on Windows)
    flask db init
    flask db migrate -m "init db"
    flask db upgrade
    python run.py createaccount
    ```
4. Start server
    ```
    python run.py
    ```
Now you can go to http://127.0.0.1:5000/
