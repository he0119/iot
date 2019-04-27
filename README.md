# IOT

Simple try for home automation using Python, Flask, Angular, SocketIO, Arduino

## Requirements

* Python 3.6+
* Node.js 8.x or 10.x

## Getting Started

1. Setup python environment

```shell
cd Flask
python -m venv venv
. venv/bin/activate(venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

1. Setup angular environment and build

```shell
  cd Angular
  npm install -g @angular/cli
  npm install
  ng build --prod
```

1. Configuration

* Rename `.env.example` to `.env` in flask folder and finish configuration
* Init database

  ```shell
  flask db init
  flask db migrate -m "init db"
  flask db upgrade
  flask createaccount
  ```

1. Start server

```shell
flask run
```

Now you can go to <http://127.0.0.1:5000/>
