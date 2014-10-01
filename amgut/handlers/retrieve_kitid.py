from amgut.lib.mail import send_email
from amgut.handlers.base_handlers import BaseHandler
from amgut.util import AG_DATA_ACCESS
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut import media_locale



class KitIDHandler(BaseHandler):
    def get(self):
        self.render('retrieve_kitid.html', message='', output='form',
                    loginerror='')

    def post(self):
        email = self.get_argument('email')
        if email:
            kitids = AG_DATA_ACCESS.getAGKitIDsByEmail(email)
        try:
            if len(kitids) > 0:
                MESSAGE = ('Your %(shorthand)s Kit IDs are %(ids)s. You are '
                           'receiving this email because you requested your '
                           'Kit ID from the %(shorthand)s web page If you did '
                           'not request your Kit ID please email '
                           '%(help_email)s Thank you,\n The '
                           '%(shorthand)s Team\n' %
                           {'ids': ", ".join(kitids),
                            'help_email': media_locale['HELP_EMAIL'],
                            'shorthand': AMGUT_CONFIG.project_shorthand})
                try:
                    send_email(MESSAGE, 'American Gut Kit ID', email)
                    self.render('retrieve_kitid.html', message='',
                                output='success', loginerror='')
                except:
                    self.render('retrieve_kitid.html', message=MESSAGE,
                                output='noemail', loginerror='')
            else:
                self.render('retrieve_kitid.html', message='nokit',
                            output='form', loginerror='')

        except:
            self.render('retrieve_kitid.html', message='', output='exception',
                        loginerror='')
