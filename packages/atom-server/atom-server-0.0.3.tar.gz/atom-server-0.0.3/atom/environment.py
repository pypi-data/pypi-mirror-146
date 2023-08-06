import abc
from http import HTTPStatus

import os

import traceback

from atom.core.Request import Request
from atom.core.Response import HttpResponse
from atom.core.AppSource import AppSource
from atom import settings
from atom.core.URLController import URLController


# takes environ and build response
class ResponseBuilder:
    request = None

    @staticmethod
    def build(environ):
        try:
            # keep request reference
            ResponseBuilder.request = Request(environ)
            return URLController().load_response(ResponseBuilder.request)
        except Exception as e:
            lines = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            print(lines)
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR).on_response()


class Application(abc.ABC):

    def __init__(self, source, **kwargs):
        self._source = source
        self._registry = []
        self._controller = None
        self.on_registry()

    @abc.abstractmethod
    def on_registry(self):
        pass

    @abc.abstractmethod
    def on_urls(self):
        pass

    def load_urls(self, controller):
        self._controller = controller
        self.on_urls()
        self._controller = None

    def register(self, subject, **kwargs):
        self._registry.append(subject)

    def get_registry(self, match_class):
        registry_classes = []
        for object_class in self._registry:
            if match_class in type.mro(object_class):
                registry_classes.append(object_class)
        return registry_classes

    def any(self, uri, methods, subject):
        return self._controller.add_url(self, uri, methods or ['GET', 'POST', 'PUT', "DELETE", 'PATCH'], subject)

    def get(self, uri, subject):
        return self._controller.add_url(self, uri, ['GET'], subject)

    def post(self, uri, subject):
        return self._controller.add_url(self, uri, ['POST'], subject)

    def put(self, uri, subject):
        return self._controller.add_url(self, uri, ['PUT'], subject)

    def patch(self, uri, subject):
        return self._controller.add_url(self, uri, ['PATCH'], subject)

    def delete(self, uri, subject):
        return self._controller.add_url(self, uri, ['DELETE'], subject)

    def status(self, status_code, route):
        return self._controller.add_status(self, status_code, route)


class AppManager:

    @staticmethod
    def get_apps():
        app_sources = get_apps_sources(False)
        return [_.get_application() for _ in app_sources]

    @staticmethod
    def get_app(app_name, is_internal):
        for app in AppManager.get_apps():
            source = app.get_source()
            if source.app_name == app_name and source.is_internal == is_internal:
                return app
        return None


def get_apps_sources(is_internal):
    directory = settings.APPS_DIRECTORY
    cwd = os.path.abspath(os.getcwd())
    path = os.path.join(cwd, directory)
    apps = []

    if os.path.exists(path):
        for file in os.listdir(path):
            if not file.startswith('.'):
                app_dir = os.path.join(cwd, directory, file)
                if os.path.isdir(app_dir):
                    manifest = os.path.join(cwd, directory, file, 'manifest.json')
                    init = os.path.join(cwd, directory, file, 'app.py')
                    location = os.path.join(cwd, directory, file)
                    if os.path.exists(manifest) and os.path.exists(init):
                        apps.append(AppSource(file, location, is_internal))
    return apps
