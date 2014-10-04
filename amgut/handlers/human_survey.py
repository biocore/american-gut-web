import os
import binascii
from json import loads, dumps

from wtforms import Form
from tornado.web import authenticated
from future.utils import viewitems
from natsort import natsorted
from json import loads, dumps
import os
import binascii
from datetime import date

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.util import store_survey
from amgut.lib.survey_supp import primary_human_survey
from amgut import r_server, text_locale, media_locale


tl = text_locale['human_survey.html']


def make_human_survey_class(group):
    """Creates a form class for a group of questions

    The top-level attributes of the generated class correspond to the question_ids from
    amgut.lib.human_survey_supp structures

    Select fields are generated for questions that require a single response, and sets
    of checkboxes for questions that can have multiple responses
    """
    attrs = {}
    prompts = {}
    for question in group.questions:
        qid = '_'.join(group.american_name.split() + [str(question.id)])

        prompts[qid] = question.question

        for i, element in enumerate(question.interface_elements):
            element_id = '%s_%d' % (qid, i)
            attrs[element_id] = element

    attrs['prompts'] = prompts
    return type('HumanSurvey', (Form,), attrs)


surveys = [make_human_survey_class(group)
           for group in primary_human_survey.groups]


class HumanSurveyHandler(BaseHandler):
    @authenticated
    def post(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        page_number = int(self.get_argument('page_number'))

        if human_survey_id is None:
            if page_number == -1:
                # http://wyattbaldwin.com/2014/01/09/generating-random-tokens-in-python/
                human_survey_id = binascii.hexlify(os.urandom(8))
                self.set_secure_cookie('human_survey_id', human_survey_id)
            else:
                # it should not be possible to get here, unless someone is
                # posting data to the page using a different interface
                self.clear_cookie('human_survey_id')
                return

        next_page_number = page_number + 1

        if page_number >= 0:
            form_data = surveys[page_number]()

            form_data.process(data=self.request.arguments)
            # TODO: collect supplemental responses

            # TODO: store supplemental data in data
            data = {'questions': form_data.data}

            r_server.hset(human_survey_id, page_number, dumps(data))

        progress = int(100.0*(page_number+2)/(len(primary_human_survey.groups) + 1))

        # if this is not the last page, render the next page
        if next_page_number < len(surveys):
            # TODO: populate the next form page from database values, if they
            # exist
            the_form = surveys[next_page_number]()
            title = primary_human_survey.groups[next_page_number].name

            supp = {}

            self.render('human_survey.html', the_form=the_form,
                        skid=self.current_user, TITLE=title,
                        supplementals=supp,
                        page_number=next_page_number,
                        progress=progress)
        else:
            # TODO: store in the database a connection between human_survey_id and this specific participant. THIS IS NOT CURRENTLY STUBBED OUT IN STORE_SURVEY

            # only get the cookie if you complete the survey
            login_id = AG_DATA_ACCESS.get_user_for_kit(self.current_user)
            print human_survey_id
            print login_id
            self.clear_cookie('human_survey_id')
            self.set_secure_cookie('completed_survey_id', human_survey_id)
            store_survey(primary_human_survey, login_id, human_survey_id)
            self.redirect(media_locale['SITEBASE'] +
                          '/authed/human_survey_completed/')
