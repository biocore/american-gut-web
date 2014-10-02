from tornado.web import RequestHandler

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
        from traceback import format_exception
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br />" % line for line in
                                 format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: %s<br />" %
                                   (k, self.request.__dict__[k]) for k in
                                    self.request.__dict__.keys()])
            error = exc_info[1]

            self.render('error.html', error=error, trace_info=trace_info,
                        request_info=request_info,
                        skid=self.current_user)


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
