# IOT
Simple try for home automation using Python, Flask, Angular, MQTT, Arduino

## Requirements
* Python 3.6.5
* Node.js 8.11.1

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

    - Rename ```py.example.conf``` to ```py.conf``` in configuration folder and finish configuration
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
