from mock import Mock
try:
    from urllib.parse import urlencode
except ImportError:  # py3
    from urllib.parse import urlencode

from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from amgut.webserver import AGWebApplication
from amgut.handlers.base_handlers import BaseHandler


class TestHandlerBase(AsyncHTTPTestCase, LogTrapTestCase):
    orig_func = BaseHandler.get_current_user

    def tearDown(self):
        #THIS WAS CAUSING GET_SECURE_COOKIE ERROR
        #BaseHandler.get_current_user = self.orig_func
        super(TestHandlerBase, self).tearDown()

    def get_app(self):
        self.app = AGWebApplication()
        return self.app

    def mock_login(self, user):
        BaseHandler.get_current_user = Mock(return_value=user)

    def get(self, url, data=None, headers=None):
        if isinstance(data, dict):
                data = urlencode(data)
        return self.fetch(url, method='GET', body=data, headers=headers)

    def post(self, url, data, headers=None):
        if isinstance(data, dict):
                data = urlencode(data)
        return self.fetch(url, method='POST', body=data, headers=headers)
