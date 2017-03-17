# This Python file uses the following encoding: utf-8
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from collections import defaultdict

from wtforms import (SelectField, SelectMultipleField, widgets,
                     TextAreaField, TextField)

from amgut import AMGUT_CONFIG
from amgut.lib.data_access.sql_connection import TRN

_LOCALE_TO_COLUMN = {'american_gut': 'american',
                     'british_gut': 'british'}


_LOCALE_COLUMN = _LOCALE_TO_COLUMN[AMGUT_CONFIG.locale]


class Question(object):
    _survey_question_table = 'survey_question'
    _question_response_table = 'survey_question_response'
    _response_table = 'survey_response'
    _response_type_table = 'survey_question_response_type'
    _supplemental_survey_table = 'survey_question_triggers'

    def __init__(self, ID, group_name):
        with TRN:
            self.id = ID
            self.group_name = group_name
            self.set_response = None

            sql = """SELECT sr.{0}
                     FROM {1} q
                     JOIN {2} qr
                         ON q.survey_question_id = qr.survey_question_id
                     JOIN {3} sr
                         ON qr.response = sr.{0}
                     WHERE q.survey_question_id = %s
                     ORDER BY qr.display_index
                  """.format(_LOCALE_COLUMN, self._survey_question_table,
                             self._question_response_table,
                             self._response_table)
            TRN.add(sql, [self.id])
            self.responses = TRN.execute_fetchflatten()

            if not self.responses:
                self.responses = None

            sql = """SELECT survey_response_type
                     FROM {0}
                     WHERE survey_question_id = %s
                  """.format(self._response_type_table)
            TRN.add(sql, [self.id])
            self.response_type = TRN.execute_fetchlast()

            sql = """SELECT {0}
                     FROM {1}
                     WHERE survey_question_id = %s
                  """.format(_LOCALE_COLUMN, self._survey_question_table)
            TRN.add(sql, [self.id])
            self.question = TRN.execute_fetchlast()

            sql = """SELECT american
                     FROM {0}
                     WHERE survey_question_id = %s
                  """.format(self._survey_question_table)
            TRN.add(sql, [self.id])
            self.american_question = TRN.execute_fetchlast()

            self.triggers = self._triggers()
            self.qid = '_'.join(self.group_name.split() + [str(self.id)])

            element_ids, elements = self._interface_elements()
            self.interface_elements = elements
            self.interface_element_ids = ['%s_%d' % (self.qid, i)
                                          for i in element_ids]

    def _triggers(self):
        """What other question-response combinations this question can trigger

        Returns
        -------
        tuple
            (other_question_id, [triggering indices to that question])
        """
        with TRN:
            sql = """SELECT triggered_question, display_index
                     FROM {0} sst
                     JOIN {1} sqr
                        ON sst.survey_question_id=sqr.survey_question_id
                        AND sqr.response=sst.triggering_response
                     WHERE sst.survey_question_id = %s
                     ORDER BY triggered_question
                 """.format(self._supplemental_survey_table,
                            self._question_response_table)
            TRN.add(sql, [self.id])
            trigger_list = TRN.execute_fetchindex()

            results = defaultdict(list)
            for question, index in trigger_list:
                results[question].append(index)

            if results:
                return results
            else:
                return ()

    def _interface_elements(self):
        """Can be overridden by subclasses"""
        return ([], [])

    @classmethod
    def factory(cls, ID, name):
        """Return the correct class type based on response type"""
        question = Question(ID, name)

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

        return question_class(question.id, name)


class QuestionSingle(Question):
    """A question where there is one response
    """
    def _interface_elements(self):
        """See superclass documentation
        """
        return ([0], [SelectField(
            self.id, choices=list(enumerate(self.responses)),
            coerce=lambda x: x)])


class QuestionMultiple(Question):
    """A question where there are multiple responses
    """
    def _interface_elements(self):
        """See superclass documentation
        """
        choices = [(i, v) for i, v in enumerate(self.responses)
                   if v != 'Unspecified']
        return ([0], [SelectMultipleField(
            self.id, choices=choices,
            widget=widgets.TableWidget(),
            option_widget=widgets.CheckboxInput(),
            coerce=lambda x: x)])


class QuestionText(Question):
    """A free-response question
    """
    def _interface_elements(self):
        """See superclass documentation
        """
        return ([0], [TextAreaField(self.id)])


class QuestionString(Question):
    """A single text field question"""
    def _interface_elements(self):
        """See superclass documentation
        """
        return ([0], [TextField(self.id)])


class Group(object):
    """Holds a logically connected group of questions

    Parameters
    ----------
    ID : int
        The ID in the database of the question group
    """
    _group_table = 'survey_group'
    _group_questions_table = 'group_questions'
    _questions_table = 'survey_question'

    def __init__(self, ID):
        with TRN:
            self.id = ID
            n = self.american_name

            sql = """SELECT gq.survey_question_id
                     FROM {0} sg
                     JOIN {1} gq ON sg.group_order = gq.survey_group
                     LEFT JOIN {2} sq USING (survey_question_id)
                     WHERE sg.group_order = %s AND sq.retired = FALSE
                     ORDER BY gq.display_index
                  """.format(self._group_table, self._group_questions_table,
                             self._questions_table)
            TRN.add(sql, [self.id])
            results = TRN.execute_fetchindex()
            qs = [Question.factory(x[0], n) for x in results]

            self.id_to_eid = {q.id: q.interface_element_ids for q in qs}

            self.question_lookup = {q.id: q for q in qs}
            self.questions = qs

            self.supplemental_eids = set()
            for q in qs:
                for id_ in q.triggers:
                    triggered = self.question_lookup[id_]
                    triggered_eids = triggered.interface_element_ids
                    self.supplemental_eids.update(set(triggered_eids))

    @property
    def name(self):
        """Gets the locale-specific name of the group"""
        with TRN:
            sql = """SELECT {0}
                     FROM {1}
                     WHERE group_order = %s""".format(_LOCALE_COLUMN,
                                                      self._group_table)
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()

    @property
    def american_name(self):
        """Gets the locale-specific name of the group"""
        with TRN:
            sql = """SELECT american
                     FROM {0}
                     WHERE group_order = %s""".format(self._group_table)
            TRN.add(sql, [self.id])
            return TRN.execute_fetchlast()


class Survey(object):
    """Represents a whole survey

    Parameters
    ----------
    ID : int
        The ID of the survey in the database
    """
    _surveys_table = 'surveys'
    _survey_response_table = 'survey_response'
    _survey_question_response_table = 'survey_question_response'
    _survey_question_response_type_table = 'survey_question_response_type'
    _survey_answers_table = 'survey_answers'
    _survey_answers_other_table = 'survey_answers_other'
    _questions_table = 'survey_question'

    def __init__(self, ID):
        self.id = ID
        with TRN:
            sql = """SELECT survey_group
                     FROM {0}
                     WHERE survey_id = %s
                     ORDER BY survey_group""".format(self._surveys_table)
            TRN.add(sql, [self.id])
            results = TRN.execute_fetchflatten()
            self.groups = [Group(x) for x in results]

            self.questions = {}
            self.question_types = {}
            for group in self.groups:
                for question in group.questions:
                    self.question_types[question.id] = question.response_type
                    self.questions[question.id] = question

            sql = """SELECT {0}
                     FROM {1}
                     WHERE american='Unspecified'
                  """.format(_LOCALE_COLUMN, self._survey_response_table)
            TRN.add(sql)
            self.unspecified = TRN.execute_fetchlast()

    def fetch_survey(self, survey_id):
        """Return {element_id: answer}

        The answer is in the form of ["display_index"] or ["text"] depending on
        if the answer has a foreign key or not. These data are serialized for
        input into a WTForm.
        """
        with TRN:
            sql = """SELECT survey_question_id, display_index,
                            survey_response_type
                     FROM {0}
                     JOIN {1} USING (response, survey_question_id)
                     JOIN {2} USING (survey_question_id)
                     LEFT JOIN {3} USING (survey_question_id)
                     WHERE survey_id = %s AND retired = FALSE""".format(
                self._survey_answers_table,
                self._survey_question_response_table,
                self._survey_question_response_type_table,
                self._questions_table)
            TRN.add(sql, [survey_id])
            answers = TRN.execute_fetchindex()

            TRN.add("""SELECT survey_question_id, response
                       FROM {0}
                       LEFT JOIN {1} using (survey_question_id)
                       WHERE survey_id = %s AND retired = FALSE""".format(
                self._survey_answers_other_table, self._questions_table),
                [survey_id])
            answers_other = TRN.execute_fetchindex()

            survey = defaultdict(list)
            print(answers)
            for qid, idx, qtype in answers:
                print(qid, idx, qtype)
                eid = self.questions[qid].interface_element_ids[0]
                print(eid)
                if qtype == 'SINGLE':
                    survey[eid] = idx
                else:
                    survey[eid].append(idx)

            for qid, data in answers_other:
                eid = self.questions[qid].interface_element_ids[0]
                data = data.strip(' []"')
                survey[eid] = data

            if len(survey) == 0:
                raise ValueError("Survey answers do not exist in DB: %s" %
                                 survey_id)
            return survey

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
        with TRN:
            TRN.add("""SELECT EXISTS(
                       SELECT 1
                       FROM ag_login_surveys
                       WHERE survey_id=%s)""",
                    [consent_details['survey_id']])

            if TRN.execute_fetchlast():
                # if the survey exists, remove all its current answers
                TRN.add("""DELETE FROM survey_answers
                               WHERE survey_id=%s""",
                        [consent_details['survey_id']])
                TRN.add("""DELETE FROM survey_answers_other
                               WHERE survey_id=%s""",
                        [consent_details['survey_id']])
            else:
                # otherwise, we have a new survey
                # If this is a primary survey, we need to add the consent
                if 'secondary' not in consent_details:
                    TRN.add("""INSERT INTO ag_consent
                                   (ag_login_id, participant_name, is_juvenile,
                                    parent_1_name, parent_2_name,
                                    deceased_parent, participant_email,
                                    assent_obtainer, age_range, date_signed)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                                     NOW())""",
                            (consent_details['login_id'],
                             consent_details['participant_name'],
                             consent_details['is_juvenile'],
                             consent_details['parent_1_name'],
                             consent_details['parent_2_name'],
                             consent_details['deceased_parent'],
                             consent_details['participant_email'],
                             consent_details['obtainer_name'],
                             consent_details['age_range']))

                TRN.add("""INSERT INTO ag_login_surveys
                               (ag_login_id, survey_id, participant_name)
                           VALUES (%s, %s, %s)""",
                        (consent_details['login_id'],
                         consent_details['survey_id'],
                         consent_details['participant_name']))

            # now we insert the answers
            TRN.add("""INSERT INTO survey_answers
                           (survey_id, survey_question_id, response)
                       VALUES (%s, %s, %s)""", with_fk_inserts, many=True)
            TRN.add("""INSERT INTO survey_answers_other
                           (survey_id,survey_question_id, response)
                       VALUES (%s, %s, %s)""", without_fk_inserts, many=True)
