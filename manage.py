#!env/bin/python

import os
import sys

if __name__ == "__main__":

    sys.path[0] = os.path.abspath("./src")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
