from os.path import dirname, join
from base64 import b64encode
from uuid import uuid4

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from amgut.handlers.base_handlers import (
    MainHandler, NoPageHandler, DBErrorHandler)
from amgut import AMGUT_CONFIG

from amgut.handlers.auth_handlers import (
    AuthRegisterHandoutHandler, AuthLoginHandler, AuthLogoutHandler)
from amgut.handlers.help_request import HelpRequestHandler
from amgut.handlers.addendum import AddendumHandler
from amgut.handlers.sample_overview import SampleOverviewHandler
from amgut.handlers.FAQ import FAQHandler
from amgut.handlers.participant_overview import ParticipantOverviewHandler
from amgut.handlers.international import InternationalHandler
from amgut.handlers.animal_survey import (AnimalSurveyHandler,
                                          CheckParticipantName)
from amgut.handlers.add_sample import (AddHumanSampleHandler,
                                       AddGeneralSampleHandler,
                                       AddAnimalSampleHandler)
from amgut.handlers.new_participant import NewParticipantHandler
from amgut.handlers.new_participant_overview import (
    NewParticipantOverviewHandler)
from amgut.handlers.taxa_summary import TaxaSummaryHandler
from amgut.handlers.survey import SurveyMainHandler
from amgut.handlers.portal import PortalHandler
from amgut.handlers.retrieve_kitid import KitIDHandler
from amgut.handlers.forgot_password import ForgotPasswordHandler
from amgut.handlers.add_sample_overview import AddSampleOverviewHandler
from amgut.handlers.change_pass_verify import ChangePassVerifyHandler

define("port", default=8888, help="run on the given port", type=int)


DIRNAME = dirname(__file__)
STATIC_PATH = join(DIRNAME, "static")
TEMPLATE_PATH = join(DIRNAME, "templates")  # base folder for webpages
RES_PATH = join(DIRNAME, "results")
COOKIE_SECRET = b64encode(uuid4().bytes + uuid4().bytes)
DEBUG = True


class QiimeWebApplication(Application):
    def __init__(self):
        handlers = [
            (r"/results/(.*)", StaticFileHandler,
             {"path": AMGUT_CONFIG.base_data_dir}),
            (r"/static/(.*)", StaticFileHandler, {"path": STATIC_PATH}),
            (r"/", MainHandler),
            (r"/db_error/", DBErrorHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/auth/register/", AuthRegisterHandoutHandler),
            (r"/authed/help_request/", HelpRequestHandler),
            (r"/authed/addendum/", AddendumHandler),
            (r"/authed/new_participant/", NewParticipantHandler),
            (r"/authed/new_participant_overview/",
                NewParticipantOverviewHandler),
            (r"/authed/sample_overview/", SampleOverviewHandler),
            (r"/authed/add_sample_overview/", AddSampleOverviewHandler),
            (r"/authed/survey_main/", SurveyMainHandler),
            (r"/authed/portal/", PortalHandler),
            (r"/authed/add_sample_human/", AddHumanSampleHandler),
            (r"/authed/add_sample_animal/", AddAnimalSampleHandler),
            (r"/authed/add_sample_general/", AddGeneralSampleHandler),
            (r"/faq/", FAQHandler),
            (r"/participants/(.*)", ParticipantOverviewHandler),
            (r"/international_shipping/", InternationalHandler),
            (r"/add_animal/", AnimalSurveyHandler),
            (r"/check_participant_name/", CheckParticipantName),
            (r"/taxa_summaries/(.*)", TaxaSummaryHandler),
            (r"/retrieve_kitid/", KitIDHandler),
            (r"/forgot_password/", ForgotPasswordHandler),
            (r"/change_pass_verify/", ChangePassVerifyHandler),
            # 404 PAGE MUST BE LAST IN THIS LIST!
            (r".*", NoPageHandler)
        ]
        settings = {
            "template_path": TEMPLATE_PATH,
            "debug": DEBUG,
            "cookie_secret": COOKIE_SECRET,
            "login_url": "/auth/login/",
        }
        super(QiimeWebApplication, self).__init__(handlers, **settings)


def main():
    parse_command_line()
    http_server = HTTPServer(QiimeWebApplication())
    http_server.listen(options.port)
    print("Tornado started on port", options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
