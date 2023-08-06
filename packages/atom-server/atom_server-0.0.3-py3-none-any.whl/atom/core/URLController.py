from http import HTTPStatus

from atom import environment
from atom.commons import regex
from atom.core.Response import HttpResponse


class URLController:

    def __init__(self):
        self.response_resources = []
        self.codes = dict()
        # attach app/module resources aka urls
        for app in environment.AppManager.get_apps():
            app.load_urls(self)

    def add_url(self, application, uri, methods, resource):
        response_resource = ResponseResource(application, uri, methods, resource)
        self.response_resources.append(response_resource)
        return response_resource

    def add_status(self, application, status, resource):
        response_resource = ResponseResource(application, None, None, resource)
        self.codes[str(status)] = response_resource
        return response_resource

    def create_response_by_status(self, request, status):
        # find custom response resource
        resource = self.codes.get(str(status))
        if resource:
            res_obj = resource.build()
            response = res_obj.on_response(request)
            response.status = status
            return response
        return HttpResponse(None, status=status).on_response()

    def load_response(self, request):
        for response_resource in self.response_resources:
            is_matched, params, pattern = regex.matchURI(response_resource.uri, request.path)
            if is_matched:
                if request.method in response_resource.methods:
                    # keep path parameters reference in Request
                    request.path = params
                    request.pattern = pattern
                    return response_resource.build().on_response(request).on_response()
                else:
                    return self.create_response_by_status(request, HTTPStatus.METHOD_NOT_ALLOWED)
        return self.create_response_by_status(request, HTTPStatus.NOT_FOUND)


class ResponseResource:

    def __init__(self, application, uri, methods, resource):
        self.application = application
        self.uri = uri
        self.methods = methods
        self.resource = resource

    def build(self):
        return self.resource(self.application)
