import logging
import posixpath
import urlparse

from future.utils import viewitems

try:
    from open_humans_tornado_oauth2 import OpenHumansMixin
except ImportError:
    logging.warn('Unable to load OpenHumansMixin, please install '
                 'open_humans_tornado_oauth2')

    OpenHumansMixin = object

from tornado import escape, web

from amgut.connections import ag_data
from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.config_manager import AMGUT_CONFIG


def basejoin(base, url):
    """
    Add the specified relative URL to the supplied base URL.

    >>> tests = [
    ...     ('https://abc.xyz',    'd/e'),
    ...     ('https://abc.xyz/',   'd/e'),
    ...     ('https://abc.xyz',    '/d/e'),
    ...     ('https://abc.xyz/',   '/d/e'),
    ...
    ...     ('https://abc.xyz',    '/d/e?a=b'),
    ...     ('https://abc.xyz/',   '/d/e?a=b'),
    ...
    ...     ('https://abc.xyz',    'd/e/'),
    ...     ('https://abc.xyz/',   'd/e/'),
    ...     ('https://abc.xyz',    '/d/e/'),
    ...     ('https://abc.xyz/',   '/d/e/'),
    ...
    ...     ('https://abc.xyz',    'd/e/?a=b'),
    ...     ('https://abc.xyz/',   'd/e/?a=b'),
    ...
    ...     ('https://abc.xyz/f',  'd/e/'),
    ...     ('https://abc.xyz/f/', 'd/e/'),
    ...     ('https://abc.xyz/f',  '/d/e/'),
    ...     ('https://abc.xyz/f/', '/d/e/'),
    ...
    ...     ('https://abc.xyz/f',  './e/'),
    ...     ('https://abc.xyz/f/', './e/'),
    ...
    ...     ('https://abc.xyz/f',  '../e/'),
    ...     ('https://abc.xyz/f/', '../e/'),
    ...
    ...     ('https://abc.xyz/f',  'd/../e/'),
    ...     ('https://abc.xyz/f/', 'd/../e/'),
    ...     ('https://abc.xyz/f',  '/d/../e/'),
    ...     ('https://abc.xyz/f/', '/d/../e/'),
    ... ]
    >>> for result in [basejoin(a, b) for a, b in tests]:
    ...     print result
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e
    https://abc.xyz/d/e?a=b
    https://abc.xyz/d/e?a=b
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/
    https://abc.xyz/d/e/?a=b
    https://abc.xyz/d/e/?a=b
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/d/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    https://abc.xyz/f/e/
    """
    # The base URL is authoritative: a URL like '../' should not remove
    # portions of the base URL.
    if not base.endswith('/'):
        base += '/'

    # Handle internal compactions, e.g. "./e/../d/" becomes "./d/"
    normalized_url = posixpath.normpath(url)

    # Ditto authoritativeness.
    if normalized_url.startswith('..'):
        normalized_url = normalized_url[2:]

    # Ditto authoritativeness.
    if normalized_url.startswith('/'):
        normalized_url = '.' + normalized_url

    # normpath removes an ending slash, add it back if necessary
    if url.endswith('/') and not normalized_url.endswith('/'):
        normalized_url += '/'

    join = urlparse.urljoin(base, normalized_url)
    joined_url = urlparse.urlparse(join)

    return urlparse.urlunparse((joined_url.scheme,
                                joined_url.netloc,
                                joined_url.path,
                                joined_url.params,
                                joined_url.query,
                                joined_url.fragment))


class OpenHumansHandler(BaseHandler, OpenHumansMixin):
    """
    Handles rendering the page responsible for linking barcodes to Open Humans
    accounts.
    """

    _API_URL = basejoin(AMGUT_CONFIG.open_humans_base_url, '/api')
    _HOME_URL = basejoin(AMGUT_CONFIG.open_humans_base_url, '/')
    _RESEARCH_URL = basejoin(AMGUT_CONFIG.open_humans_base_url,
                             '/member/me/research-data/')

    @web.authenticated
    @web.asynchronous
    def get(self):
        open_humans = self.get_secure_cookie('open-humans')

        # If the user isn't authenticated render the page to allow them to
        # authenticate
        if not open_humans:
            self.render('open-humans.html',
                        skid=self.current_user,
                        linked_barcodes=None,
                        unlinked_barcodes=None,
                        access_token=None,
                        open_humans_home_url=self._HOME_URL,
                        open_humans_research_url=self._RESEARCH_URL,
                        open_humans_api_url=self._API_URL)

            return

        open_humans = escape.json_decode(open_humans)

        self.open_humans_request(
            '/american-gut/user-data/',
            self._on_user_data,
            access_token=open_humans['access_token'])

    def _on_user_data(self, user_data):
        open_humans = escape.json_decode(self.get_secure_cookie('open-humans'))

        skid = self.current_user

        # At this point we just deal with human participants
        (human_participants, _, _, _) = ag_data.get_menu_items(skid)

        linked_barcodes = []
        unlinked_barcodes = []

        # Get the linked and unlinked barcodes and their participant IDs
        for participant, barcodes in viewitems(human_participants):
            for barcode in barcodes:
                barcode['participant'] = participant

                if barcode['barcode'] in user_data['barcodes']:
                    linked_barcodes.append(barcode)
                else:
                    unlinked_barcodes.append(barcode)

        self.render('open-humans.html',
                    skid=skid,
                    linked_barcodes=linked_barcodes,
                    unlinked_barcodes=unlinked_barcodes,
                    access_token=open_humans['access_token'],
                    open_humans_home_url=self._HOME_URL,
                    open_humans_research_url=self._RESEARCH_URL,
                    open_humans_api_url=self._API_URL)


class OpenHumansLoginHandler(BaseHandler, OpenHumansMixin):
    """
    Handles the OAuth2 connection to Open Humans.
    """

    _API_URL = basejoin(AMGUT_CONFIG.open_humans_base_url, '/api')

    _OAUTH_REDIRECT_URL = basejoin(AMGUT_CONFIG.base_url,
                                   'authed/connect/open-humans/')

    _OAUTH_AUTHORIZE_URL = basejoin(AMGUT_CONFIG.open_humans_base_url,
                                    '/oauth2/authorize/')
    _OAUTH_ACCESS_TOKEN_URL = basejoin(AMGUT_CONFIG.open_humans_base_url,
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
            extra_params={'scope': 'read write american-gut'})

    def _on_login(self, user):
        """
        Handle the user object from the login request.
        """
        if user:
            logging.info('logged in user from openhumans: ' + str(user))

            self.set_secure_cookie('open-humans', escape.json_encode(user))
        else:
            self.clear_cookie('open-humans')

        self.redirect('/authed/open-humans/')


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=(doctest.NORMALIZE_WHITESPACE |
                                               doctest.REPORT_NDIFF))
