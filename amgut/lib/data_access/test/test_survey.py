from unittest import TestCase, main
from wtforms.form import BaseForm
from amgut.lib.data_access.survey import (
    Question, QuestionSingle, QuestionMultiple, QuestionText, QuestionString,
    Group, Survey)


class TestQuestionSingle(TestCase):
    def test_create_no_triggers(self):
        q_single = QuestionSingle(23, 'Education')
        self.assertEqual(q_single.id, 23)
        self.assertEqual(q_single.group_name, 'Education')
        self.assertEqual(q_single.set_response, None)
        self.assertEqual(q_single.response_type, 'SINGLE')
        self.assertEqual(q_single.question,
                         'What is your highest level of education?')
        self.assertEqual(q_single.american_question,
                         'What is your highest level of education?')
        self.assertEqual(q_single.triggers, tuple())
        self.assertEqual(q_single.qid, 'Education_23')
        self.assertEqual(q_single.interface_element_ids, ['Education_23_0'])

        # Test rendering of form object
        form = BaseForm({
            q_single.interface_element_ids[0]: q_single.interface_elements[0]
        })
        eid = q_single.interface_element_ids[0]
        self.assertEqual(str(type(form[eid])),
                         "<class 'wtforms.fields.core.SelectField'>")
        self.assertEqual(
            form[eid].choices, [
                (0, 'Unspecified'),
                (1, 'Did not complete high school'),
                (2, 'High School or GED equilivant'),
                (3, 'Some college or technical school'),
                (4, "Associate's degree"),
                (5, "Bachelor's degree"),
                (6, 'Some graduate school or professional'),
                (7, 'Graduate or Professional degree')])

    def test_create_triggers(self):
        q_single = QuestionSingle()
        q_single.id
        q_single.group_name
        q_single.set_response
        q_single.response_type
        q_single.question
        q_single.american_question
        q_single.triggers
        q_single.qid
        q_single.interface_elements
        q_single.interface_element_ids

    def test_interface_elements(self):
        raise NotImplementedError()


class TestQuestionMultiple(TestCase):
    def test__interface_elements(self):
        raise NotImplementedError()


class TestQuestionText(TestCase):
    def test__interface_elements(self):
        raise NotImplementedError()


class TestQuestionString(TestCase):
    def test__interface_elements(self):
        raise NotImplementedError()


class TestGroup(TestCase):
    def test___init__(self):
        raise NotImplementedError()

    def test_name(self):
        raise NotImplementedError()

    def test_american_name(self):
        raise NotImplementedError()


class TestSurvey(TestCase):
    def test___init__(self):
        raise NotImplementedError()

    def test_fetch_survey(self):
        raise NotImplementedError()

    def test_store_survey(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
