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

./manage.py collectstatic --noinput

[ "$1" == "production" ] && { 

    # create symbolic link for use absolute path in config files
    sudo ln -sf $PWD -T /srv/memorymodel

    # use production environment
    sudo touch /srv/memorymodel/.production

    # set the right modes
    sudo chmod -R 755 /srv/memorymodel
    sudo chmod 666 /srv/memorymodel/log/debug.log

    # install apache if needed
    [ -f /etc/init.d/apache2 ] || {
        sudo apt-get -y install apache2;
    }
    sudo apt-get -y install libapache2-mod-wsgi

    # configure apache for using memorymodel website
    sudo ln -sf /srv/memorymodel/etc/apache2/sites-available/memorymodel /etc/apache2/sites-available/
    sudo a2ensite memorymodel
    sudo /etc/init.d/apache2 restart

}
