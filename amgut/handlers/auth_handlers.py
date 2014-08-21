#!/usr/bin/env python

from tornado.web import authenticated
from tornado.escape import json_encode

from amgut.util import AG_DATA_ACCESS
from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler

# login code modified from https://gist.github.com/guillaumevincent/4771570


class AuthRegisterHandoutHandler(BaseHandler):
    """User Creation"""
    @authenticated
    def get(self):
        latlong_db = AG_DATA_ACCESS.getMapMarkers()
        skid = self.get_argument("skid").strip()
        self.render("register_user.html", skid=skid, latlongs_db=latlong_db)

    @authenticated
    def post(self):
        skid = self.current_user
        password = self.get_argument('pass')
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
            ag_login_id, skid, password, kitinfo['swabs_per_kit'],
            kitinfo['kit_verification_code'], printresults)
        if success == -1:
            self.redirect('/db_error/?err=regkit')
            return

        # Add the barcodes
        ag_kit_id = kitinfo['ag_kit_id']
        results = AG_DATA_ACCESS.get_barcodes_from_handout_kit(skid)
        for row in results:
            barcode = row[0]
            success = AG_DATA_ACCESS.addAGBarcode(ag_kit_id, barcode)
            if success == -1:
                self.redirect('/db_error/?err=regbarcode')
                return



        # Email the verification code
        subject = "American Gut Verification Code"
        addendum = ''
        if kit_id.startswith('PGP_'):
            addendum = ("\n\nFor the PGP cohort, we are requesting that you "
                        "collect one sample from each of the following sites:"
                        "\n\nLeft hand\nRight hand\nForehead\nMouth\nFecal\n\n"
                        "This is important to ensure that we have the same "
                        "types of samples for all PGP participants which, in "
                        "turn, could be helpful in downstream analysis when "
                        "looking for relationships between the microbiome and "
                        "the human genome\n\n.")

        body = ("Thank you for registering with the American Gut Project! Your"
                " verification code is:\n\n{0}\n\nYou will need this code to "
                "verifiy your kit on the American Gut webstite. To get "
                "started, please log into:\n\nhttp://microbio.me/AmericanGut"
                "\n\nEnter the kit_id and password found inside your kit, "
                "verify the contents of your kit, and enter the verification "
                "code found in this email.{1}"
                "\n\nSincerely,\nThe American Gut Team".format(
                    kitinfo['kit_verification_code'], addendum))

        result = 'Kit registered successfully.'
        try:
                send_email(MESSAGE, subject, recipient=info['email'],
                           sender='americangut@gmail.com')
        except:
            result = ("There was a problem sending your email. Please "
                      "contact us directly at "
                      "<a href='mailto:info@americangut.org'>info@americangut.org</a>")

            self.render('help_request.html', skid=self.current_user,
                        result=result)

        self.redirect('/authed/portal/')


class AuthLoginHandler(BaseHandler):
    """user login, no page necessary"""
    def post(self):
        skid = self.get_argument("skid", "").strip()
        password = self.get_argument("password", "")
        login = AG_DATA_ACCESS.authenticateWebAppUser(skid, password)

        if login:
            # everything good so log in
            self.set_current_user(skid)
            self.redirect("/authed/portal/")
            return
        else:
            is_handout = AG_DATA_ACCESS.handoutCheck(skid, password)
            if is_handout == 'y':
                # login user but have them register themselves
                self.set_current_user(skid)
                self.redirect('/auth/register/')
                return
            else:
                msg = "Invalid Kit ID or Password"
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
        self.redirect("/")
