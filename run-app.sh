#! /bin/bash

sudo su
apt-get -y install python3
apt-get -y install python3-pip
python3 -m pip install -R requirements.txt
flask run -h localhost -p $1