#!/usr/bin/env python

from tornado.web import authenticated, HTTPError
from tornado.escape import json_encode
import logging

from amgut.connections import ag_data
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale, text_locale

# login code modified from https://gist.github.com/guillaumevincent/4771570
def set_current_user(self, user):
    if user:
        self.set_secure_cookie("skid", json_encode(user))
    else:
        self.clear_cookie("skid")

class AuthRegisterHandoutHandler(BaseHandler):
    """User Creation"""
    def get(self):
        skid = self.get_argument("skid").strip()
        latlong_db = ag_data.getMapMarkers()
        self.render("register_user.html", skid=skid,
                    latlongs_db=latlong_db, loginerror='')

    def post(self):
        # Check handout
        skid = self.get_argument("skid").strip()
        password = self.get_argument("password")
        is_handout = ag_data.handoutCheck(skid, password)
        if not is_handout:
            self.redirect(media_locale['SITEBASE'] +
                          "/?loginerror=Invalid%40password")
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
        set_current_user(skid)
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
        except:
            logging.exception('Error on skid %s:' % skid)


class AuthLoginHandler(BaseHandler):
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
            self.redirect(media_locale['SITEBASE'] + '/auth/register/?skid=%s'
                          % skid)
            return

        login = ag_data.authenticateWebAppUser(skid, password)
        if login:
            # everything good so log in
            set_current_user(skid)
            default_redirect = media_locale['SITEBASE'] + '/authed/portal/'
            self.redirect(self.get_argument('next', default_redirect))
            return
        else:
            msg = tl['INVALID_KITID']
            latlongs_db = ag_data.getMapMarkers()
            self.render("index.html", user=None, loginerror=msg,
                        latlongs_db=latlongs_db)
            return


class AuthLogoutHandler(BaseHandler):
    """Logout handler, no page necessary"""
    @authenticated
    def get(self):
        self.clear_cookie("skid")
        self.redirect(media_locale['SITEBASE'] + "/")
