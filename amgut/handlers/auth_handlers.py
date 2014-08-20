#!/usr/bin/env python

from tornado.web import authenticated
from tornado.escape import url_escape, json_encode

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler, _get_lat_long

# login code modified from https://gist.github.com/guillaumevincent/4771570


class AuthRegisterHandoutHandler(BaseHandler):
    """User Creation"""
    @authenticated
    def get(self):
        latlong_db = _get_lat_long()
        skid = self.get_argument("skid").strip()
        self.render("register_user.html", skid=skid, latlongs_db=latlong_db)

    @authenticated
    def post(self):
        skid = self.get_argument("kit_id")
        info = {}
        for info_column in ("email", "name", "address", "city", "state", "zip",
                            "country"):

            # Make sure that all fields were entered
            info[info_column] = self.get_argument(info_column, None)

        AG_DATA_ACCESS.addAGLogin(info['email'], info['name'],
                                  info['address'], info['city'],
                                  info['state'], info['zip'],
                                  info['country'])

        self.redirect('/authed/portal/')


class AuthLoginHandler(BaseHandler):
    """user login, no page necessary"""
    def post(self):
        skid = self.get_argument("skid", "").strip()
        password = self.get_argument("password", "")
        login = AG_DATA_ACCESS.authenticateWebAppUser(skid, password)
        print "LOGIN!!!!!", login
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
                self.redirect('/auth/register/?skid=%s' % skid)
                return
            else:
                msg = "Invalid Kit ID or Password"
                latlongs_db = _get_lat_long()
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
