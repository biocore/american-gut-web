from wtforms import Form, SelectField, SelectMultipleField, widgets
from tornado.web import authenticated
from future.utils import viewitems
from natsort import natsorted
from json import loads, dumps
from uuid import uuid4

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.human_survey_supp import (
    responses_map,  key_map, question_group, group_order, question_type,
    supplemental_map)
from amgut import r_server, text_locale


tl = text_locale['human_survey.html']


def make_human_survey_class(group):
    attrs = {}
    for idx in sorted(question_group[group]):
        question_id = key_map[idx]
        responses = responses_map[idx]

        if question_type[question_id] == 'SINGLE':
            attrs[question_id] = SelectField(
                question_id, choices=list(enumerate(responses)))

        elif question_type[question_id] == 'MULTIPLE':
            attrs[question_id] = SelectMultipleField(
                question_id, choices=list(enumerate(responses)),
                widget=widgets.TableWidget(),
                option_widget=widgets.CheckboxInput(),
                coerce=lambda x: x)

    return type('HumanSurvey', (Form,), attrs)


surveys = [make_human_survey_class(group) for group in group_order]


class HumanSurveyHandler(BaseHandler):
    @authenticated
    def post(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        page_number = int(self.get_argument('page_number'))

        if human_survey_id is None:
            if page_number == -1:
                human_survey_id = str(uuid4())
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
            r_server.hset(human_survey_id, page_number, dumps(form_data.data))

        # if this is not the last page, render the next page
        if next_page_number < len(surveys):
            self.set_secure_cookie('human_survey_page_number',
                                   str(next_page_number))
            # TODO: populate the next form page from database values, if they
            # exist
            the_form = surveys[next_page_number]()
            title = tl[group_order[next_page_number]+'_TITLE']
            self.render('human_survey.html', the_form=the_form,
                        skid=self.current_user, TITLE=title,
                        supplemental_map=supplemental_map,
                        page_number=next_page_number,
                        progress=int(100.0*(page_number+2)/len(group_order)))
        else:
            # TODO: insert into database
            self.clear_cookie('human_survey_id')
            # TODO: redirect to portal or something
