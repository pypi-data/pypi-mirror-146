import base64
import json
from http.cookies import SimpleCookie, CookieError
from urllib.parse import urlparse, parse_qs

from atom.commons.exception import HttpBadRequest, HttpUnsupportedMediaType


class Request:

    def __init__(self, environ):
        self.environ = environ
        self.uri = environ.get('RAW_URI')
        self.path = urlparse(self.uri).path
        self.method = environ.get('REQUEST_METHOD')
        self.protocol = environ.get('wsgi.url_scheme')
        self.REMOTE_ADDR = environ.get('REMOTE_ADDR')
        self.SERVER_NAME = environ.get('SERVER_NAME')
        self.HTTP_HOST = environ.get('HTTP_HOST')
        self.CONTENT_TYPE = environ.get('CONTENT_TYPE')
        self.CONTENT_LENGTH = int(environ.get('CONTENT_LENGTH', 0))
        self.HTTP_AUTHORIZATION = environ.get('HTTP_AUTHORIZATION')
        self.HTTP_USER_AGENT = environ.get('HTTP_USER_AGENT')
        self.HTTP_X_REAL_IP = environ.get('HTTP_X_REAL_IP')
        self.HTTP_X_FORWARDED_FOR = environ.get('HTTP_X_FORWARDED_FOR')
        self.HOST_URL = "{protocol}://{host}".format(protocol=self.protocol, host=self.HTTP_HOST)
        self.GET = GetMethod(self, environ)
        self.POST = PostMethod(self, environ)
        # stores path based parameters [lateinit]
        self.PATH = dict()
        # stores routing pattern [lateinit]
        self.pattern = None
        # post handle cookie headers [lateinit]
        self.cookie_headers = []

    def get_http_authorization(self):
        if self.HTTP_AUTHORIZATION:
            auth_type = self.HTTP_AUTHORIZATION.split(' ')[0]
            auth_data = self.HTTP_AUTHORIZATION.replace(auth_type, '', 1).strip()
            if auth_type == 'Basic':
                message_bytes = base64.b64decode(auth_data.encode('ascii'))
                auth_data = message_bytes.decode('ascii').split(":")
            return auth_type, auth_data
        return None, None

    def get_cookies(self):
        try:
            cookie_string = self.environ.get('HTTP_COOKIE')
            if cookie_string:
                cookie = SimpleCookie()
                cookie.load(self.environ.get('HTTP_COOKIE'))
                return dict((k, v.value) for k, v in cookie.items())
        except CookieError:
            pass
        return {}

    def set_cookie(self, name, value, **kwargs):
        self.cookie_headers.append(('Set-Cookie', f"{name}={value}"))

    def delete_cookie(self, name):
        self.cookie_headers.append(('Set-Cookie', f"{name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"))


class GetMethod:

    def __init__(self, request, environ):
        self.params = parse_qs(environ['QUERY_STRING'])

    def get(self, key, default_value=None):
        if self.params.get(key):
            return self.params.get(key)[0]
        return self.params.get(key, default_value)

    def get_int(self, key):
        try:
            return int(self.params.get(key)[0])
        except Exception:
            return None

    def get_list(self, key):
        return self.params.get(key, [])

    def __str__(self):
        return str(self.params)


class PostMethod:

    def __init__(self, request, environ):
        self.body = None

        if request.method != 'GET':
            if request.CONTENT_TYPE:
                if request.CONTENT_TYPE == 'application/x-www-form-urlencoded':
                    self.body = parse_qs(environ['wsgi.input'].read(request.CONTENT_LENGTH).decode("utf-8"))
                elif request.CONTENT_TYPE == 'application/json; charset=utf-8':
                    try:
                        self.body = json.loads(environ['wsgi.input'].read(request.CONTENT_LENGTH).decode("utf-8"))
                    except Exception:
                        raise HttpBadRequest("Invalid JSON content given.")
                else:
                    raise HttpUnsupportedMediaType()
            else:
                raise HttpUnsupportedMediaType()

    def get(self, key, default_value=None):
        if self.body.get(key):
            return self.body.get(key)[0]
        return self.body.get(key, default_value)

    def get_list(self, key):
        return self.body.get(key, [])

    def get_body(self):
        return self.body

    def __str__(self):
        return str(self.body)
