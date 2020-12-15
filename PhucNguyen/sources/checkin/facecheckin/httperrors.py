# This file contains all classes, models for processing/responding to HTTP requests
import json
import sys

from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotAllowed


class HttpErrors:
    """
    Handle exceptions/errors when there's a request to server.
    """

    METHOD_NOT_ALLOWED_405 = HttpResponseNotAllowed(
        '<h1>Error 405: Method is not supported</h1>')

    @staticmethod
    def serverErrorHandler(request=None, exception=None,
        message='', allowTraceback=False):
        """
        Handle in case error occur with current request.

        Args:
            request (json): current request to server.
            exception (): exeption.
            message (string): message to notification.
            allowTraceback (bool): allow trace back flag.
        Returns:
            errorResponse (object): http response server error object.
        """

        errorResponse = HttpResponseServerError(
            '<h1>Error 500: Internal server error</h1>')
        # if request is not None:
        #     LOGGER.info('Request URL: {0}'.format(request.path_info))
        #     # LOGGER.info('Request body: {0}'.format(request.body))
        # LOGGER.error("Error processing request: {0}.".format(exception))
        # LOGGER.error("Exception info: {0}".format(sys.exc_info()))

        errorResponse.write('<div>Message: {0}</div>'.format(message))
        errorResponse.write('<div>Exception: {0}</div>'.format(exception))
        if allowTraceback is True:
            errorResponse.write('<div>Traceback: {0}</div>'.format(sys.exc_info()))
        return errorResponse

    @staticmethod
    def badRequest(request, message=''):
        """
        Handle in case bad request to server.

        Args:
            request (json): current request to server.
            message (string): message to notification.
        Returns:
            errorResponse (object): http response bad request.
        """

        errorResponse = HttpResponseBadRequest(
            '<h1>Error 400: Bad request (invalid syntax)</h1>')

        # LOGGER.info('Request URL: {0}'.format(request.path_info))
        # LOGGER.info('Request body: {0}'.format(request.body))
        # LOGGER.info('Message: {0}'.format(message))

        errorResponse.write('<div>Message:{0}</div>'.format(message))

        return errorResponse