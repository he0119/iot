# IOT
Simple try for home automation using Python, Flask, Angular, SocketIO, Arduino

## Requirements
* Python 3.6.6
* Node.js 8.12.0

## Getting Started
1. Setup python environment
    ```bash
    virtualenv --no-site-packages --python=python3.6 venv 
    . venv/bin/activite(venv\Scripts\activate on Windows)
    pip install -r requirements.txt
    ```
2. Setup angular environment
	```bash
    cd iot/angular/iot
    npm install -g @angular/cli
    npm install
    ng build --prod
	```
3. Configuration

    - Rename ```.env.example``` to ```.env``` in root folder and finish configuration
    - Init database
    ```bash
    flask db init
    flask db migrate -m "init db"
    flask db upgrade
    flask createaccount
    ```
4. Start server
    ```bash
    flask run
    ```
Now you can go to http://127.0.0.1:5000/
## ChangeLog
### v0.2.1
* Fixed missing time field in status page
