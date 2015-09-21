import logging
import posixpath
import urlparse

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


class OriginMixin(object):
    """
    A mixin for coercing an origin from a query parameter into a valid origin.
    """

    def coerce_origin(self):
        origin = self.get_argument('origin', False)

        # if there's not a valid origin specified default to external
        if origin not in ['external', 'open-humans']:
            origin = 'external'

        return origin


class OpenHumansHandler(BaseHandler, OpenHumansMixin, OriginMixin):
    """
    Handles rendering the page responsible for linking barcodes to Open Humans
    accounts.
    """

    _API_URL = basejoin(AMGUT_CONFIG.open_humans_base_url, '/api')
    _HOME_URL = basejoin(AMGUT_CONFIG.open_humans_base_url, '/')
    _RESEARCH_URL = basejoin(AMGUT_CONFIG.open_humans_base_url,
                             '/member/me/research-data/')
    _RETURN_URL = basejoin(_HOME_URL, 'study/american-gut/return/')

    @web.authenticated
    @web.asynchronous
    def get(self):
        open_humans = self.get_secure_cookie('open-humans')

        # If the user isn't authenticated render the page to allow them to
        # authenticate
        if not open_humans:
            ag_login_id = ag_data.get_user_for_kit(self.current_user)
            human_participants = ag_data.getHumanParticipants(ag_login_id)

            survey_ids = {}

            for participant_name in human_participants:
                survey_id = ag_data.get_survey_id(ag_login_id,
                                                  participant_name)

                if survey_id:
                    survey_ids[participant_name] = survey_id

            self.render('open-humans.html',
                        skid=self.current_user,
                        survey_ids=survey_ids,
                        access_token=None,
                        origin=self.coerce_origin(),
                        open_humans_home_url=self._HOME_URL,
                        open_humans_research_url=self._RESEARCH_URL,
                        open_humans_api_url=self._API_URL)

            return

        open_humans = escape.json_decode(open_humans)

        self.open_humans_request(
            '/american-gut/user-data/',
            self._on_user_data_cb,
            access_token=open_humans['access_token'])

    def _on_post_user_data_cb(self, data):
        """
        After the survey ID has been posted to Open Humans.
        """
        self.clear_cookie('link-survey-id')

        self.redirect('{}?origin={}'.format(self._RETURN_URL,
                                            self.coerce_origin()))

    def _on_user_data_cb(self, user_data):
        open_humans = escape.json_decode(self.get_secure_cookie('open-humans'))

        try:
            link_survey_id = escape.json_decode(
                escape.url_unescape(self.get_cookie('link-survey-id')))
        except AttributeError:
            link_survey_id = None

        ag_login_id = ag_data.get_user_for_kit(self.current_user)
        human_participants = ag_data.getHumanParticipants(ag_login_id)

        survey_ids = {}

        if link_survey_id:
            self.open_humans_request(
                '/american-gut/user-data/',
                self._on_post_user_data_cb,
                method='PATCH',
                body={'data': {'surveyIds': link_survey_id}},
                access_token=open_humans['access_token'])

            return

        for participant_name in human_participants:
            survey_id = ag_data.get_survey_id(ag_login_id, participant_name)

            if survey_id:
                survey_ids[participant_name] = survey_id

        self.render('open-humans.html',
                    skid=self.current_user,
                    survey_ids=survey_ids,
                    access_token=open_humans['access_token'],
                    origin=self.coerce_origin(),
                    open_humans_home_url=self._HOME_URL,
                    open_humans_research_url=self._RESEARCH_URL,
                    open_humans_api_url=self._API_URL)


class OpenHumansLoginHandler(BaseHandler, OpenHumansMixin, OriginMixin):
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
        """
        Display the Open Humans connection page.
        """
        redirect_uri = self._OAUTH_REDIRECT_URL

        # if we have a code, we have been authorized so we can log in
        if self.get_argument('code', False):
            self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=AMGUT_CONFIG.open_humans_client_id,
                client_secret=AMGUT_CONFIG.open_humans_client_secret,
                code=self.get_argument('code'),
                callback=self._on_login_cb)
        # otherwise we need to request an authorization code
        else:
            extra_params = {
                'scope': 'read write american-gut',
                'origin': self.coerce_origin(),
            }

            self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=AMGUT_CONFIG.open_humans_client_id,
                extra_params=extra_params)

    def _on_login_cb(self, user):
        """
        Handle the user object from the login request.
        """
        if user:
            logging.info('logged in user from openhumans: ' + str(user))

            self.set_secure_cookie('open-humans', escape.json_encode(user))
        else:
            self.clear_cookie('open-humans')

        self.redirect('/authed/open-humans/?origin={}'.format(
            self.coerce_origin()))
