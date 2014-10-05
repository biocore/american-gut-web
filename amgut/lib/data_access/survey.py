#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from itertools import groupby
from operator import itemgetter

from wtforms import (SelectField, SelectMultipleField, widgets,
                     TextAreaField, TextField)

from amgut import AMGUT_CONFIG, db_conn


_LOCALE_TO_COLUMN = {'american_gut': 'american',
                     'british_gut': 'british'}


_LOCALE_COLUMN = _LOCALE_TO_COLUMN[AMGUT_CONFIG.locale]


class Question(object):
    _survey_question_table = 'survey_question'
    _question_response_table = 'survey_question_response'
    _response_table = 'survey_response'
    _response_type_table = 'survey_question_response_type'
    _supplemental_survey_table = 'survey_question_triggered_by'

    def __init__(self, ID, current_response=None):
        self.id = ID

        responses = db_conn.execute_fetchall('''
            select sr.{0}
            from {1} q join {2} qr
                on q.survey_question_id = qr.survey_question_id
            join {3} sr on qr.response = sr.{0}
            where q.survey_question_id = %s
            order by qr.display_index'''.format(
                _LOCALE_COLUMN,
                self._survey_question_table,
                self._question_response_table,
                self._response_table),
            [self.id])

        self.responses = [row[0] for row in responses]

        if not responses:
            self.responses = None

        self.response_type = db_conn.execute_fetchone('''
            select survey_response_type from {0}
            where survey_question_id = %s'''.format(
                self._response_type_table),
            [self.id])[0]

        self.question = db_conn.execute_fetchone('''
            select {0}
            from {1}
            where survey_question_id = %s'''.format(
                _LOCALE_COLUMN,
                self._survey_question_table),
                [self.id])[0]

        self.triggered_by = self._triggered_by()

    def _triggered_by(self):
        """What other question-response combinations trigger this question

        Returns
        -------
        dict
            {other_question_id: [triggering responses to that question], ...}
        """
        trigger_list = db_conn.execute_fetchall('''
            select trigger_question, trigger_response
            from survey_question_triggered_by
            where survey_question_id = %s
            order by trigger_question'''.format(
                self._supplemental_survey_table),
            [self.id])

        return {key: list(group)
                for key, group in groupby(trigger_list, key=itemgetter(0))}

    @property
    def interface_elements(self):
        """Get WTForms interface elements for the question

        Returns
        -------
        list
            A list of the elements that represent the interface to the question
        """
        raise NotImplementedError("To be implemented by quesiton subtypes.")


class QuestionSingle(Question):
    """A question where there is one response
    """
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionSingle, self).__init__(survey_question_id,
                                             current_response)

    @property
    def interface_elements(self):
        """See superclass documentation
        """
        return [SelectField(
            self.id, choices=list(enumerate(self.responses)),
            coerce=lambda x: x)]


class QuestionMultiple(Question):
    """A question where there are multiple responses
    """
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionMultiple, self).__init__(survey_question_id,
                                               current_response)
    @property
    def interface_elements(self):
        """See superclass documentation
        """
        choices = [(i,v) for i, v in enumerate(self.responses)
                   if v != 'Unspecified']
        return [SelectMultipleField(
            self.id, choices=choices,
            widget=widgets.TableWidget(),
            option_widget=widgets.CheckboxInput(),
            coerce=lambda x: x)]


class QuestionText(Question):
    """A free-response question
    """
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionText, self).__init__(survey_question_id,
                                           current_response)

    @property
    def interface_elements(self):
        """See superclass documentation
        """
        return [TextAreaField(self.id)]


class QuestionString(Question):
    """A single text field question"""
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionString, self).__init__(survey_question_id,
                                             current_response)

    @property
    def interface_elements(self):
        """See superclass documentation
        """
        return [TextField(self.id)]


class Group(object):
    """Holds a logically connected group of questions

    Parameters
    ----------
    ID : int
        The ID in the database of the question group
    """
    _group_table = 'survey_group'
    _group_questions_table = 'group_questions'

    def __init__(self, ID):
        self.id = ID
        qs = [Question(x[0]) for x in db_conn.execute_fetchall('''
            select gq.survey_question_id
            from {0} sg join {1} gq on sg.group_order = gq.survey_group
            where sg.group_order = %s
            order by gq.display_index
            '''.format(
                self._group_table,
                self._group_questions_table),
            [self.id])]

        self.questions = []
        for question in qs:
            response_type = question.response_type
            question_class = None

            if response_type == 'SINGLE':
                question_class = QuestionSingle
            elif response_type == 'MULTIPLE':
                question_class = QuestionMultiple
            elif response_type == 'TEXT':
                question_class = QuestionText
            elif response_type == 'STRING':
                question_class = QuestionString
            else:
                raise ValueError("Unrecognized response type: %s" %
                                 response_type)

            self.questions.append(question_class(question.id))

    @property
    def name(self):
        """Gets the locale-specific name of the group
        """
        return db_conn.execute_fetchone('''
            select {0}
            from {1} where group_order = %s'''.format(
                _LOCALE_COLUMN,
                self._group_table),
            [self.id])[0]

    @property
    def american_name(self):
        """Gets the locale-specific name of the group
        """
        return db_conn.execute_fetchone('''
            select american
            from {0} where group_order = %s'''.format(
                self._group_table),
            [self.id])[0]


class Survey(object):
    """Represents a whole survey

    Parameters
    ----------
    ID : int
        The ID of the survey in the database
    """
    _surveys_table = 'surveys'
    _survey_answer_table = 'survey_response'

    def __init__(self, ID):
        self.id = ID

        self.groups = [Group(x[0]) for x in db_conn.execute_fetchall('''
            select survey_group
            from {0} where survey_id = %s
            order by survey_group'''.format(
                self._surveys_table),
            [self.id])]

        self.questions = {}
        self.question_types = {}
        for group in self.groups:
            for question in group.questions:
                self.question_types[question.id] = question.response_type
                self.questions[question.id] = question

        self.unspecified = db_conn.execute_fetchone("""
            select {0}
            from {1}
            where american='Unspecified'""".format(
                _LOCALE_COLUMN,
                self._survey_answer_table))[0]

    def store_survey(self, consent_details, with_fk_inserts,
                     without_fk_inserts):
        """Store a survey

        Parameters
        ----------
        consent_details : dict
            Participant consent details
        with_fk_inserts : list
            [(str, int, str)] where str is the survey_id, int is a
            survey_question.survey_question_id and str is a
            survey_response.american
        without_fk_inserts : list
            [(str, int, str)] where str is the survey_id, int is a
            survey_question.survey_question_id and str is a json representation
            of the data to insert
        """
        with db_conn.get_postgres_cursor() as cur:
            cur.execute("""
                INSERT INTO ag_consent
                    (ag_login_id, participant_name, is_juvenile,
                     parent_1_name, parent_2_name, deceased_parent,
                     participant_email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (consent_details['login_id'],
                         consent_details['participant_name'],
                         consent_details['is_juvenile'],
                         consent_details['parent_1_name'],
                         consent_details['parent_2_name'],
                         consent_details['deceased_parent'],
                         consent_details['participant_email']))

            cur.execute("""
                INSERT INTO ag_login_surveys
                    (ag_login_id, survey_id, participant_name)
                VALUES (%s, %s, %s)""",
                        (consent_details['login_id'],
                         consent_details['survey_id'],
                         consent_details['participant_name']))

            cur.executemany("""
                INSERT INTO survey_answers (survey_id, survey_question_id,
                                            response)
                VALUES (%s, %s, %s)""",
                            with_fk_inserts)
            cur.executemany("""
                            INSERT INTO survey_answers_other (survey_id,
                                                survey_question_id, response)
                            VALUES (%s, %s, %s)""",
                            without_fk_inserts)

    #def get_survey(self, survey_id):
    #    """Get a survey given a survey id"""
    #    new_survey
