from http import HTTPStatus


class CoreException(Exception):

    def __init__(self, message, status, tag):
        super().__init__(message)
        self.message = message
        self.status = status
        self.tag = tag


class HttpMethodNotAllowed(CoreException):

    def __init__(self, message=None, tag=None):
        super().__init__(message, HTTPStatus.METHOD_NOT_ALLOWED, tag)


class HttpInternalServerError(CoreException):

    def __init__(self, message=None, tag=None):
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR, tag)


class HttpNotImplemented(CoreException):

    def __init__(self, message=None, tag=None):
        super().__init__(message, HTTPStatus.NOT_IMPLEMENTED, tag)


class HttpUnsupportedMediaType(CoreException):

    def __init__(self, message=None, tag=None):
        super().__init__(message, HTTPStatus.UNSUPPORTED_MEDIA_TYPE, tag)


class HttpBadRequest(CoreException):

    def __init__(self, message=None, tag=None):
        super().__init__(message, HTTPStatus.BAD_REQUEST, tag)
