import json
import os
import importlib.util


class AppSource:

    def __init__(self, app_name, app_location, is_internal):
        self.app_name = app_name
        self.app_location = app_location
        self.is_internal = is_internal

    def get_application(self):
        module_file = os.path.join(self.app_location, 'app.py')
        return AppSource.load_instance(module_file).App(self)

    @staticmethod
    def load_instance(module_file):
        spec = importlib.util.spec_from_file_location("module.init", module_file)
        obj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(obj)
        return obj

    def get_manifest(self):
        return json.loads(open(os.path.join(self.app_location, 'manifest.json'), 'r').read())

    def get_template_directory(self):
        return os.path.join(self.app_location, 'templates')