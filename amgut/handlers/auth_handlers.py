#!/usr/bin/env python

from tornado.web import authenticated
from tornado.escape import json_encode

from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale, text_locale

# login code modified from https://gist.github.com/guillaumevincent/4771570


class AuthRegisterHandoutHandler(BaseHandler):
    """User Creation"""
    @authenticated
    def get(self):
        latlong_db = AG_DATA_ACCESS.getMapMarkers()
        self.render("register_user.html", skid=self.current_user,
                    latlongs_db=latlong_db, loginerror='')

    @authenticated
    def post(self):
        skid = self.current_user
        tl=text_locale['handlers']
        info = {}
        for info_column in ("email", "participantname", "address", "city",
                            "state", "zip", "country"):
            # Make sure that all fields were entered
            info[info_column] = self.get_argument(info_column, None)

        # create the user if needed
        ag_login_id = AG_DATA_ACCESS.addAGLogin(
            info['email'], info['participantname'], info['address'],
            info['city'], info['state'], info['zip'], info['country'])
        # Create the kit and add the kit to the user
        kitinfo = AG_DATA_ACCESS.getAGHandoutKitDetails(skid)
        printresults = AG_DATA_ACCESS.checkPrintResults(skid)
        if printresults is None:
            printresults = 'n'
        success = AG_DATA_ACCESS.addAGKit(
            ag_login_id, skid, kitinfo['password'],
            kitinfo['swabs_per_kit'], kitinfo['verification_code'],
            printresults)
        if success == -1:
            self.redirect(media_locale['SITEBASE'] + '/db_error/?err=regkit')
            return

        # Add the barcodes
        kitinfo = AG_DATA_ACCESS.getAGKitDetails(skid)
        ag_kit_id = kitinfo['ag_kit_id']
        results = AG_DATA_ACCESS.get_barcodes_from_handout_kit(skid)
        for row in results:
            barcode = row[0]
            success = AG_DATA_ACCESS.addAGBarcode(ag_kit_id, barcode)
            if success == -1:
                self.redirect(media_locale['SITEBASE'] + '/db_error/?err=regbarcode')
                return

        # Email the verification code
        subject = tl['AUTH_SUBJECT']
        addendum = ''
        if skid.startswith('PGP_'):
            addendum = tl['AUTH_REGISTER_PGP']

        body = tl['AUTH_REGISTER_BODY'].format(
            kitinfo['kit_verification_code'], addendum)

        result = tl['KIT_REG_SUCCESS']
        try:
            send_email(body, subject, recipient=info['email'],
                       sender=media_locale['HELP_EMAIL'])
        except:
            result = media_locale['EMAIL_ERROR']

            self.render('help_request.html', skid=skid, result=result)

        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')


class AuthLoginHandler(BaseHandler):
    """user login, no page necessary"""
    def post(self):
        skid = self.get_argument("skid", "").strip()
        password = self.get_argument("password", "")
        tl = text_locale['handlers']
        login = AG_DATA_ACCESS.authenticateWebAppUser(skid, password)
        if login:
            # everything good so log in
            self.set_current_user(skid)
            self.redirect(media_locale['SITEBASE'] + "/authed/portal/")
            return
        else:
            is_handout = AG_DATA_ACCESS.handoutCheck(skid, password)
            if is_handout == 'y':
                # login user but have them register themselves
                self.set_current_user(skid)
                self.redirect(media_locale['SITEBASE'] + '/auth/register/')
                return
            else:
                msg = tl['INVALID_KITID']
                latlongs_db = AG_DATA_ACCESS.getMapMarkers()
                self.render("index.html", user=None, loginerror=msg,
                            latlongs_db=latlongs_db)
                return

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("skid", json_encode(user))
        else:
            self.clear_cookie("skid")


class AuthLogoutHandler(BaseHandler):
    """Logout handler, no page necessary"""
    def get(self):
        self.clear_cookie("skid")
        self.redirect(media_locale['SITEBASE'] + "/")
