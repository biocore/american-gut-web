from wtforms import Form, SelectField, SelectMultipleField
from tornado.web import authenticated
from future.utils import viewitems
from natsort import natsorted
from json import loads, dumps
from uuid import uuid4

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
# TODO: fix this import to reflect reality
from amgut.lib import question_map as qm, question_group
from amgut import r_server, text_locale


tl = text_locale['human_survey.html']


# responses_map === idx: choices for that index
# question_group === group: list of indices, where group is something like GENERAL_DIET_INFORMATION
# key_map === idx: key of question
# group_order === [group]

# question_type === key: {SINGLE, MULTIPLE}
# supplemental_map === key:

def make_human_survey_class(group):
    attrs = {}
    for idx in sorted(question_group[group]):
        question_id = key_map[idx]
        responses = response_map[idx]

        if question_type[question_id] == 'SINGLE':
            attrs[question_id] = SelectField(
                question_id, choices=list(enumerate(responses)))

        elif question_type[question_id] == 'MULTIPLE':
            attrs[question_id] = SelectMultipleField(
                question_id, choices=list(enumerate(responses)),
                coerce=lambda x: x)

    return type('HumanSurvey', (Form,), attrs)


surveys = [make_human_survey_class(group) for group in group_order]


class HumanSurveyHandler(BaseHandler):
    @authenticated
    def get(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        page_number = self.get_secure_cookie('human_survey_page_number') or 0

        if human_survey_id is None:
            self.set_secure_cookie('human_survey_id', uuid4())
            page_number = 0

        self.set_secure_cookie('human_survey_page_number', page_number)

        # TODO: populate the next form page from database values, if they
        # exist
        the_form = surveys[page_number]()
        title = tl[group_order[page_number]+'_TITLE']
        self.render('human_survey.html', the_form=the_form,
                    page_number=page_number, title=TITLE)

    @authenticated
    def post(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        page_number = self.get_secure_cookie('human_survey_page_number')
        if human_survey_id is None or page_number is None:
            self.redirect('/')
            return

        next_page_number = page_number + 1

        form_data = surveys[page_number]()
        form_data.process(data=self.request.arguments)
        r_server.rpush(human_survey_id, dumps(form_data.data))

        # if this is not the last page, render the next page
        if next_page_number < len(surveys):
            # TODO: populate the next form page from database values, if they
            # exist
            the_form = surveys[next_page_number]()
            self.render('human_survey.html', the_form=the_form,
                        page_number=next_page_number)
        else:
            # TODO: insert into database
            self.clear_cookie('human_survey_id')
            self.clear_cookie('human_survey_page_number')
            self.render('portal.html', msg="hopefully success")
