import logging

from tornado.web import RequestHandler, StaticFileHandler

from amgut.connections import ag_data
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.mail import send_email
from amgut import text_locale


class BaseHandler(RequestHandler):
    def get_current_user(self):
        """Overrides default method of returning user currently connected"""
        skid = self.get_secure_cookie("skid")
        if skid is None:
            self.clear_cookie("skid")
            return None
        else:
            return skid.strip('" ')

    def write_error(self, status_code, **kwargs):
        """Overrides the error page created by Tornado"""
        from traceback import format_exception
        user = self.current_user
        # render error page BEFORE handling the error
        if user:
            self.render('error.html', skid=user)
        else:
            self.render('no_auth_error.html', loginerror="")

        logging.exception(kwargs["exc_info"])
        exc_info = kwargs["exc_info"]
        trace_info = ''.join(format_exception(*exc_info))
        request_info = ''.join(["%s:   %s\n" %
                               (k, self.request.__dict__[k]) for k in
                                self.request.__dict__])
        error = exc_info[1]
        formatted_email = (">SKID\n%s\n\n>Error\n%s\n\n>Traceback\n%s\n\n"
                           ">Request Info\n%s\n\n" %
                           (user, error, trace_info, request_info))

        send_email(formatted_email, "SERVER ERROR!",
                   recipient=AMGUT_CONFIG.error_email)

    def head(self):
        """Satisfy servers that this url exists"""
        self.finish()


class MainHandler(BaseHandler):
    """Index page"""
    def get(self):
        latlong_db = ag_data.getMapMarkers()
        self.render("index.html", latlongs_db=latlong_db, loginerror="")


class NoPageHandler(BaseHandler):
    """404 page"""
    def get(self):
        self.set_status(404)
        if self.current_user:
            self.render("404.html", skid=self.current_user)
        else:
            self.render("no_auth_404.html", loginerror="")

    def head(self):
        """Satisfy servers that this url exists"""
        self.set_status(404)
        self.finish()


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
