import abc
from atom.commons.exception import HttpNotImplemented, HttpInternalServerError


class URLRoute(abc.ABC):

    def __init__(self, application):
        super(URLRoute, self).__init__()
        self.application = application

    def on_response(self, request):
        if request.method == 'GET':
            return self.on_get(request)
        elif request.method == 'POST':
            return self.on_post(request)
        elif request.method == 'DELETE':
            return self.on_delete(request)
        elif request.method == 'PUT':
            return self.on_put(request)
        elif request.method == 'PATCH':
            return self.on_put(request)
        raise HttpNotImplemented("Not implemented HTTP %s method" % request.method)

    def on_get(self, request):
        raise HttpInternalServerError("%s method response undefined" % request.method)

    def on_post(self, request):
        raise HttpInternalServerError("%s method response undefined" % request.method)

    def on_delete(self, request):
        raise HttpInternalServerError("%s method response undefined" % request.method)

    def on_put(self, request):
        raise HttpInternalServerError("%s method response undefined" % request.method)

    def on_patch(self, request):
        raise HttpInternalServerError("%s method response undefined" % request.method)
