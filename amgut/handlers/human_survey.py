from json import dumps
from collections import defaultdict

from wtforms import Form
from tornado.web import authenticated

from amgut.handlers.base_handlers import BaseHandler
from amgut.lib.util import store_survey
from amgut.lib.survey_supp import primary_human_survey
from amgut import r_server, media_locale


def make_human_survey_class(group):
    """Creates a form class for a group of questions

    The top-level attributes of the generated class correspond to the question_ids from
    amgut.lib.human_survey_supp structures

    Select fields are generated for questions that require a single response, and sets
    of checkboxes for questions that can have multiple responses
    """
    attrs = {}
    prompts = {}
    triggers = defaultdict(list)
    triggered = defaultdict(list)

    for q in group.questions:
        for eid, element in zip(q.interface_element_ids, q.interface_elements):
            attrs[eid] = element
            prompts[eid] = q.question

            if q.triggers:
                for triggered_id, triggering_responses in q.triggers.items():
                    triggers[eid].extend(triggering_responses)
                    triggered[eid].extend(group.id_to_eid[triggered_id])

    attrs['prompts'] = prompts
    attrs['triggers'] = triggers
    attrs['triggered'] = triggered
    attrs['supplemental_eids'] = group.supplemental_eids

    return type('HumanSurvey', (Form,), attrs)


surveys = [make_human_survey_class(group)
           for group in primary_human_survey.groups]


class HumanSurveyHandler(BaseHandler):
    @authenticated
    def post(self):
        human_survey_id = self.get_secure_cookie('human_survey_id')
        page_number = int(self.get_argument('page_number'))
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
            # only get the cookie if you complete the survey
            self.clear_cookie('human_survey_id')
            self.set_secure_cookie('completed_survey_id', human_survey_id)
            store_survey(primary_human_survey, human_survey_id)
            self.redirect(media_locale['SITEBASE'] +
                          '/authed/human_survey_completed/')
