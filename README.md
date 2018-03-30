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
	npm install
    ng build --prod
	```
3. Start server
    ```
    python run.py
    ```
Now you can go to http://127.0.0.1:5000/
