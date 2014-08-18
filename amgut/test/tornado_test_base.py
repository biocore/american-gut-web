from mock import Mock
try:
    from urllib import urlencode
except ImportError:  # py3
    from urllib.parse import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from amgut.webserver import Application
from amgut.handlers.base_handlers import BaseHandler


class TestHandlerBase(AsyncHTTPTestCase):
    database = False

    def get_app(self):
        BaseHandler.get_current_user = Mock(return_value="test@foo.bar")
        self.app = Application()
        return self.app

    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def tearDown(self):
        pass

    # helpers from http://www.peterbe.com/plog/tricks-asynchttpclient-tornado
    def get(self, url, data=None, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)
            if '?' in url:
                url += '&amp;%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers=headers)

    def post(self, url, data, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)
        return self._fetch(url, 'POST', data, headers)

    def _fetch(self, url, method, data=None, headers=None):
        self.http_client.fetch(self.get_url(url), self.stop, method=method,
                               body=data, headers=headers)
        return self.wait()
