#!/usr/bin/env python

from tornado.web import authenticated
from tornado.escape import json_encode
import logging
from collections import defaultdict

from amgut.connections import ag_data
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale, text_locale


# login code modified from https://gist.github.com/guillaumevincent/4771570
class AuthBasehandler(BaseHandler):
    def set_current_user(self, user=None):
        if user is not None:
            self.set_secure_cookie("skid", json_encode(user))
        else:
            self.clear_cookie("skid")


class AuthRegisterHandoutHandler(AuthBasehandler):
    """User Creation"""

    def get(self):
        kit_counts = ag_data.getMapMarkers()
        countries = ag_data.get_countries()

        # defaults entries dict to be empty
        entries = defaultdict(str)
        self.render("register_user.html", kit_counts=kit_counts,
                    loginerror='', countries=countries, entries=entries)

    def post(self):
        # Check handout
        skid = self.get_argument("kit_id").strip()
        password = self.get_argument("password")

        is_handout = ag_data.handoutCheck(skid, password)
        if not is_handout:
            kit_counts = ag_data.getMapMarkers()
            countries = ag_data.get_countries()
            entries = {'kit_id': self.get_argument('kit_id'),
                       'email': self.get_argument('email'),
                       'email2': self.get_argument('email2'),
                       'participantname': self.get_argument('participantname'),
                       'address': self.get_argument('address'),
                       'city': self.get_argument('city'),
                       'state': self.get_argument('state'),
                       'zip': self.get_argument('zip'),
                       'country': self.get_argument('country')}
            self.render("register_user.html", kit_counts=kit_counts,
                        loginerror='', countries=countries, entries=entries)
            return

        # Register handout
        tl = text_locale['handlers']
        info = {
            "email": self.get_argument("email"),
            "participantname": self.get_argument("participantname")
        }
        for info_column in ("address", "city", "state", "zip", "country"):
            # Make sure that all fields were entered
            info[info_column] = self.get_argument(info_column, None)

        # create the user if needed
        ag_login_id = ag_data.addAGLogin(
            info['email'], info['participantname'], info['address'],
            info['city'], info['state'], info['zip'], info['country'])
        # Create the kit and add the kit to the user
        success = ag_data.registerHandoutKit(ag_login_id, skid)
        if not success:
            self.redirect(media_locale['SITEBASE'] + '/db_error/?err=regkit')
            return

        # log user in since registered successfully
        self.set_current_user(skid)
        self.redirect(media_locale['SITEBASE'] + "/authed/portal/")

        kitinfo = ag_data.getAGKitDetails(skid)

        # Email the verification code
        # send email after redirect since it takes so long
        subject = tl['AUTH_SUBJECT']
        addendum = ''
        if skid.startswith('PGP_'):
            addendum = tl['AUTH_REGISTER_PGP']

        body = tl['AUTH_REGISTER_BODY'].format(
            kitinfo['kit_verification_code'], addendum)
        try:
            send_email(body, subject, recipient=info['email'],
                       sender=media_locale['HELP_EMAIL'])
        except BaseException:
            logging.exception('Error on skid %s:' % skid)


class AuthLoginHandler(AuthBasehandler):
    """user login, no page necessary"""

    def get(self, *args, **kwargs):
        self.redirect(media_locale['SITEBASE'] + "/")

    def post(self):
        skid = self.get_argument("skid", "").strip()
        password = self.get_argument("password", "")
        tl = text_locale['handlers']

        is_handout = ag_data.handoutCheck(skid, password)
        if is_handout:
            # have them register themselves
            self.redirect(media_locale['SITEBASE'] + '/?loginerror=' +
                          tl['REGISTER_KIT'])

            return

        login = ag_data.authenticateWebAppUser(skid, password)
        if login:
            # everything good so log in
            self.set_current_user(skid)
            default_redirect = media_locale['SITEBASE'] + '/authed/portal/'
            self.redirect(self.get_argument('next', default_redirect))
            return
        else:
            msg = tl['INVALID_KITID']
            kit_counts = ag_data.getMapMarkers()
            self.render("index.html", user=None, loginerror=msg,
                        kit_counts=kit_counts)
            return


class AuthLogoutHandler(AuthBasehandler):
    """Logout handler, no page necessary"""
    @authenticated
    def get(self):
        self.set_current_user()
        self.redirect(media_locale['SITEBASE'] + "/")
