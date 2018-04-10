#!/usr/bin/env python

from os.path import dirname, join

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options, parse_command_line

from amgut import media_locale

from amgut.handlers.base_handlers import (
    MainHandler, NoPageHandler, DBErrorHandler, BaseStaticFileHandler)
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
from amgut.handlers.human_survey import HumanSurveyHandler
from amgut.handlers.human_survey_completed import HumanSurveyCompletedHandler
from amgut.handlers.vioscreen import VioscreenPassthroughHandler
from amgut.handlers.add_sample import (AddHumanSampleHandler,
                                       AddGeneralSampleHandler,
                                       AddAnimalSampleHandler)
from amgut.handlers.new_participant import NewParticipantHandler
from amgut.handlers.new_participant_overview import (
    NewParticipantOverviewHandler)
from amgut.handlers.taxa_summary import TaxaSummaryHandler
from amgut.handlers.survey import SurveyMainHandler
from amgut.handlers.secondary_survey import SecondarySurveyHandler
from amgut.handlers.personal_microbiome_overview import \
        PersonalMicrobiomeOverviewHandler
from amgut.handlers.portal import PortalHandler
from amgut.handlers.retrieve_kitid import KitIDHandler
from amgut.handlers.forgot_password import ForgotPasswordHandler
from amgut.handlers.add_sample_overview import AddSampleOverviewHandler
from amgut.handlers.change_pass_verify import ChangePassVerifyHandler
from amgut.handlers.change_password import ChangePasswordHandler
from amgut.handlers.nojs import NoJSHandler
from amgut.handlers.download import DownloadHandler

from amgut.handlers.open_humans import (OpenHumansHandler,
                                        OpenHumansLoginHandler)
from amgut.handlers.interactive import (
    MultiSampleHandler, MetadataHandler, AlphaDivImgHandler)
from amgut.lib.startup_tests import startup_tests

define("port", default=8888, help="run on the given port", type=int)


DIRNAME = dirname(__file__)
STATIC_PATH = join(DIRNAME, "static")
TEMPLATE_PATH = join(DIRNAME, "templates")  # base folder for webpages
RES_PATH = join(DIRNAME, "results")
DEBUG = True


class AGWebApplication(Application):
    def __init__(self):
        handlers = [
            (r"/static/(.*)", BaseStaticFileHandler, {"path": STATIC_PATH}),
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
            (r"/authed/human_survey/", HumanSurveyHandler),
            (r"/authed/human_survey_completed/", HumanSurveyCompletedHandler),
            (r"/authed/vspassthrough/", VioscreenPassthroughHandler),
            (r"/authed/secondary_survey/", SecondarySurveyHandler),
            (r"/authed/personal_microbiome_overview/",
             PersonalMicrobiomeOverviewHandler),
            (r"/authed/portal/", PortalHandler),
            (r"/authed/add_sample_human/", AddHumanSampleHandler),
            (r"/authed/add_sample_animal/", AddAnimalSampleHandler),
            (r"/authed/add_sample_general/", AddGeneralSampleHandler),
            (r"/authed/change_password/", ChangePasswordHandler),
            (r"/authed/add_animal/", AnimalSurveyHandler),
            (r"/authed/open-humans/", OpenHumansHandler),
            (r"/authed/connect/open-humans/", OpenHumansLoginHandler),
            (r"/authed/download/(.*)", DownloadHandler),
            # (r"/authed/single/", SingleSampleHandler),
            (r"/authed/multiple/", MultiSampleHandler),
            (r"/interactive/metadata/", MetadataHandler),
            (r"/interactive/alpha_div/(.*)", AlphaDivImgHandler),
            (r"/faq/", FAQHandler),
            (r"/participants/(.*)", ParticipantOverviewHandler),
            (r"/international_shipping/", InternationalHandler),
            (r"/check_participant_name/", CheckParticipantName),
            (r"/authed/taxa_summaries/(.*)", TaxaSummaryHandler),
            (r"/retrieve_kitid/", KitIDHandler),
            (r"/forgot_password/", ForgotPasswordHandler),
            (r"/change_pass_verify/", ChangePassVerifyHandler),
            (r"/nojs/", NoJSHandler),
            # 404 PAGE MUST BE LAST IN THIS LIST!
            (r".*", NoPageHandler)
        ]
        settings = {
            "template_path": TEMPLATE_PATH,
            "debug": DEBUG,
            "cookie_secret": AMGUT_CONFIG.cookie_secret,
            # Currently the only login form is on the homepage
            "login_url": media_locale['SITEBASE'] + '/',
        }
        super(AGWebApplication, self).__init__(handlers, **settings)


def main():
    startup_tests()
    # replace spaces for underscores to autocomplete easily in a shell
    # format looks like american_gut_8888.log
    prefix = (join(AMGUT_CONFIG.base_log_dir, "%s_%d.log" %
              (media_locale['LOCALE'], options.port)).replace(' ', '_'))
    options.log_file_prefix = prefix
    options.logging = 'warning'
    parse_command_line()
    http_server = HTTPServer(AGWebApplication())
    http_server.listen(options.port)
    print("Tornado started on port", options.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
