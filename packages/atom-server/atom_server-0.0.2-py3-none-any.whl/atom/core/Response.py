import json
import abc
from http import HTTPStatus


class ResponseData:

    def __init__(self, headers, status, response_body):
        self.headers = headers
        self.status = status
        self.response_body = response_body

    def get_status(self):
        return str(self.status.value) + ' ' + self.status.phrase


class Response(abc.ABC):

    def __init__(self, **kwargs):
        self.headers = kwargs.get('headers', [])
        self.status = kwargs.get('status', HTTPStatus.OK)

    @abc.abstractmethod
    def on_response(self) -> ResponseData:
        pass


class HttpResponse(Response):

    def __init__(self, body=None, **kwargs):
        super(HttpResponse, self).__init__(**kwargs)
        self.body = body or ""
        self.headers.append(('Content-Type', 'text/plain'))

    def on_response(self):
        response_body = bytes(self.body, 'utf-8')
        return ResponseData(self.headers, self.status, response_body)


class JSONResponse(Response):

    def __init__(self, body=None, **kwargs):
        super(JSONResponse, self).__init__(**kwargs)
        self.body = body or {}
        self.pretty_print = kwargs.get('pretty_print', False)
        self.headers.append(('Content-Type', 'application/json'))

    def on_response(self):
        if self.pretty_print:
            response_body = bytes(json.dumps(self.body, indent=4), 'utf-8')
        else:
            response_body = bytes(json.dumps(self.body), 'utf-8')
        return ResponseData(self.headers, self.status, response_body)