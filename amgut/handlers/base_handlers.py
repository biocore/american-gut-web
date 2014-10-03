import logging

from tornado.web import RequestHandler, StaticFileHandler

from amgut.util import AG_DATA_ACCESS
from amgut import text_locale


class BaseHandler(RequestHandler):
    def get_current_user(self):
        '''Overrides default method of returning user curently connected'''
        skid = self.get_secure_cookie("skid")
        if skid is None:
            self.clear_cookie("skid")
            return None
        else:
            return skid.strip('" ')

    def write_error(self, status_code, **kwargs):
        '''Overrides the error page created by Tornado'''
        logging.exception(kwargs["exc_info"])
        self.render('error.html', skid=self.current_user)


class MainHandler(BaseHandler):
    '''Index page'''
    def get(self):
        latlong_db = AG_DATA_ACCESS.getMapMarkers()
        self.render("index.html", latlongs_db=latlong_db, loginerror="")


class NoPageHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.render("404.html", skid=self.current_user)
        else:
            self.render("no_auth_404.html", loginerror="")


class DBErrorHandler(BaseHandler):
    def get(self):
        err = self.get_argument('err')
        tl = text_locale['handlers']
        errors = {
            "regkit": tl['ADD_KIT_ERROR'],
            "regbarcode": tl['ADD_BARCODE_ERROR']
        }
        if err not in errors:
            raise ValueError('DB Error not found: %s' % err)
        self.render("db_error.html", skid=self.current_user,
                    message=errors[err])

class BaseStaticFileHandler(StaticFileHandler, BaseHandler):
    def write_error(self, status_code, **kwargs):
        if self.current_user:
            self.render("404.html", skid=self.current_user)
        else:
            self.render("no_auth_404.html", loginerror="")
