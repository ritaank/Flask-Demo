#! /bin/bash

echo "NOTICE: building environment"
sudo apt update
sudo apt-get -y install python3
sudo add-apt-repository universe
sudo apt -y install python3-pip

sudo apt -y install python3-flask
sudo apt-get -y install python3-sqlalchemy
pip3 install Flask-SQLAlchemy
pip3 install -r requirements.txt
sudo apt -y install curl

export FLASK_APP="app.py"
echo "NOTICE: initializing flask app on port ${1:-3000}"
flask run -h localhost -p ${1:-3000} #if no port specified, default port: 3000
