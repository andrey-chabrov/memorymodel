#!/bin/bash

# using pip and virtualenv
sudo apt-get -y install python-pip python-virtualenv python-dev

# install db
cd db
psql -U postgres -f drop.sql
psql -U postgres -f create.sql
cd ..

virtualenv --no-site-packages --python=python2.7 env
env/bin/pip install -r requirements.txt

./manage.py syncdb --noinput
./manage.py migrate