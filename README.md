# IOT
Simple try for home automation using Python, Flask, Angular, MQTT, Arduino

## Requirements
* Python 3.6.5
* Node.js 8.10.0

## Getting Started
1. Setup python environment
    ```bash
    virtualenv --no-site-packages venv
    source venv/bin/activite(venv\Scripts\activate on Windows)
    pip install -r requirements.txt
    ```
2. Setup angular environment
	
	```bash
    cd iot\angular
    npm install -g @angular/cli
	npm install
    ng build --prod
	```
3. Configuration
    
    - Create a ```py.conf``` file in configuration folder
    ```ini
    [admin]
    #info about your account
    username=example
    password=example
    email=hello@example.com

    [mqtt]
    #I currently use shiftr.io
    id=mqtt client id
    username=broker username
    password=broker password
    url=broker.shiftr.io
    port=8883
    ```
    - Init database
    ```bash
    export FLASK_APP=run.py(set FLASK_APP=run.py on Windows)
    flask db init
    flask db migrate -m "init db"
    flask db upgrade
    flask createaccount
    ```
4. Start server
    ```bash
    python run.py
    ```
Now you can go to http://127.0.0.1:5000/
