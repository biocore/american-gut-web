import logging

from urlparse import urljoin

try:
    from open_humans_tornado_oauth2 import OpenHumansMixin
except ImportError:
    OpenHumansMixin = object

from tornado import escape, web

from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.config_manager import AMGUT_CONFIG


class OpenHumansHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('open-humans.html', skid=self.current_user)


class OpenHumansLoginHandler(BaseHandler, OpenHumansMixin):
    _OAUTH_REDIRECT_URL = urljoin(AMGUT_CONFIG.base_url,
                                  '/authed/connect/open-humans/')

    _OAUTH_AUTHORIZE_URL = urljoin(AMGUT_CONFIG.open_humans_base_url,
                                   '/oauth2/authorize/')
    _OAUTH_ACCESS_TOKEN_URL = urljoin(AMGUT_CONFIG.open_humans_base_url,
                                      '/oauth2/token/')

    @web.authenticated
    @web.asynchronous
    def get(self):
        redirect_uri = self._OAUTH_REDIRECT_URL

        # if we have a code, we have been authorized so we can log in
        if self.get_argument('code', False):
            self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=AMGUT_CONFIG.open_humans_client_id,
                client_secret=AMGUT_CONFIG.open_humans_client_secret,
                code=self.get_argument('code'),
                callback=self._on_login)

            return

        # otherwise we need to request an authorization code
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=AMGUT_CONFIG.open_humans_client_id,
            extra_params={'scope': 'read+write'})

    def _on_login(self, user):
        """
        This handles the user object from the login request
        """
        if user:
            logging.info('logged in user from openhumans: ' + str(user))

            self.set_secure_cookie('user', escape.json_encode(user))
        else:
            self.clear_cookie('user')

        self.redirect('/authed/open-humans/')


# TODO: Connect this
class OpenHumansConnectionHandler(BaseHandler, OpenHumansMixin):
    _API_URL = urljoin(AMGUT_CONFIG.open_humans_base_url, '/api')

    @web.authenticated
    @web.asynchronous
    def get(self):
        self.open_humans_request(
            '/american-gut/user-data/current/',
            self._on_user_data,
            access_token=self.current_user['access_token'])

    def _on_user_data(self, user_data):
        if user_data is None:
            # Session may have expired
            self.redirect('/authed/connect/open-humans/')

            return

        self.render('open-humans.html', user_data=user_data)
