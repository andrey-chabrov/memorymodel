#!env/bin/python

import os
import sys

if __name__ == "__main__":

    sys.path[0] = os.path.abspath("./src")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    import memorymodel
    from memorymodel.generator import ModelFromYaml

    # Use this path and app_label for example.
    path = os.path.join(os.path.dirname(memorymodel.generator.__file__), 'models.yaml')
    app_label = 'memorymodel'
    ModelFromYaml()(path, app_label)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
