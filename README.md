# IOT
Simple try for home automation using Python, Flask, Angular, SocketIO, Arduino

## Requirements
* Python 3.7.1
* Node.js 10.14.1

## Getting Started
1. Setup python environment
    ```bash
    cd flask/iot
    virtualenv --no-site-packages venv
    . venv/bin/activate(venv\Scripts\activate on Windows)
    pip install -r requirements.txt
    ```
2. Setup angular environment and build
	```bash
    cd angular/iot
    npm install -g @angular/cli
    npm install
    ng build --prod
	```
3. Configuration

    - Rename ```.env.example``` to ```.env``` in flask folder and finish configuration
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
