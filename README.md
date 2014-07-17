memorymodel
===========

Operates with Django model classes saved in memory from yaml.

Main code block that creates a models located in ./src/memorymodel/generator.py
module.

Installation:
    1) Install PostgreSQL server at first.
    2) Test mode:
        . bootstrap.sh
       Production mode:
       . bootstrap.sh production

Test the application:
./manage.py test

Serve the application:
./manage.py runserver