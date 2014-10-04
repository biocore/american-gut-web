#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

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

        if current_response is None:
            pass
            # TODO: something

    @property
    def triggered_by(self):
        # should return question_id: responses

        things = db_conn.execute_fetchone('''
            select exists(select * from survey_question_triggered_by
            where survey_question_id = %s)''', self.id)

        raise NotImplementedError("We are about to do this (probably)...")


class QuestionSingle(Question):
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionSingle, self).__init__(survey_question_id,
                                             current_response)
        # TODO: something


class QuestionMultiple(Question):
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionMultiple, self).__init__(survey_question_id,
                                               current_response)
        # TODO: something


class QuestionText(Question):
    def __init__(self, survey_question_id, current_response=None):
        super(QuestionText, self).__init__(survey_question_id,
                                           current_response)
        # TODO: something


class Group(object):
    _group_table = 'survey_group'
    _group_questions_table = 'group_questions'

    def __init__(self, ID):
        self.id = ID
        # TODO: probably this can be better
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
            else:
                raise ValueError("Unrecognized response type: %s" %
                                 response_type)

            self.questions.append(question_class(question.id))

    @property
    def name(self):
        """Gets the locale-specific name of the group
        """
        return db_conn.execute_fetchone('''
            select {0}_name
            from {1} where group_order = %s'''.format(
                _LOCALE_COLUMN,
                self._group_table),
            [self.id])[0]

    @property
    def american_name(self):
        """Gets the locale-specific name of the group
        """
        return db_conn.execute_fetchone('''
            select american_name
            from {0} where group_order = %s'''.format(
                self._group_table),
            [self.id])[0]


class Survey(object):
    _surveys_table = 'surveys'

    def __init__(self, ID):
        self.id = ID

        self.groups = [Group(x[0]) for x in db_conn.execute_fetchall('''
            select survey_group
            from {0} where survey_id = %s
            order by survey_group'''.format(
                self._surveys_table),
            [self.id])]
