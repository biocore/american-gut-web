from unittest import TestCase, main
from wtforms.form import BaseForm
from amgut.lib.data_access.survey import (
    QuestionSingle, QuestionMultiple, QuestionText, QuestionString)
# Question, Group, Survey)


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
        q_single = QuestionSingle(20, 'dog')
        self.assertEqual(q_single.id, 20)
        self.assertEqual(q_single.group_name, 'dog')
        self.assertEqual(q_single.set_response, None)
        self.assertEqual(q_single.response_type, 'SINGLE')
        self.assertEqual(q_single.question, 'Do you have a dog(s)?')
        self.assertEqual(q_single.american_question, 'Do you have a dog(s)?')
        self.assertEqual(q_single.triggers, {101: [1], 105: [1]})
        self.assertEqual(q_single.qid, 'dog_20')
        self.assertEqual(q_single.interface_element_ids, ['dog_20_0'])

        # Test form object
        form = BaseForm({
            q_single.interface_element_ids[0]: q_single.interface_elements[0]
        })
        eid = q_single.interface_element_ids[0]
        self.assertEqual(str(type(form[eid])),
                         "<class 'wtforms.fields.core.SelectField'>")
        self.assertEqual(
            form[eid].choices, [(0, 'Unspecified'), (1, 'Yes'), (2, 'No')])


class TestQuestionMultiple(TestCase):
    def test_create(self):
        q_multi = QuestionMultiple(30, 'Alcohol')
        self.assertEqual(q_multi.id, 30)
        self.assertEqual(q_multi.group_name, 'Alcohol')
        self.assertEqual(q_multi.set_response, None)
        self.assertEqual(q_multi.response_type, 'MULTIPLE')
        self.assertEqual(q_multi.question,
                         'What type(s) of alcohol do you typically consume '
                         '(select all that apply)?')
        self.assertEqual(q_multi.american_question,
                         'What type(s) of alcohol do you typically consume '
                         '(select all that apply)?')
        self.assertEqual(q_multi.triggers, tuple())
        self.assertEqual(q_multi.qid, 'Alcohol_30')
        self.assertEqual(q_multi.interface_element_ids, ['Alcohol_30_0'])

        # Test rendering of form object
        form = BaseForm({
            q_multi.interface_element_ids[0]: q_multi.interface_elements[0]
        })
        eid = q_multi.interface_element_ids[0]
        self.assertEqual(str(type(form[eid])),
                         "<class 'wtforms.fields.core.SelectMultipleField'>")
        self.assertEqual(
            form[eid].choices, [
                (0, 'Beer/Cider'),
                (1, 'Sour beers'),
                (2, 'White wine'),
                (3, 'Red wine'),
                (4, 'Spirits/hard alcohol')])


class TestQuestionText(TestCase):
    def test_create(self):
        q_text = QuestionText(98, 'Pregnancy')
        self.assertEqual(q_text.id, 98)
        self.assertEqual(q_text.group_name, 'Pregnancy')
        self.assertEqual(q_text.set_response, None)
        self.assertEqual(q_text.response_type, 'TEXT')
        self.assertEqual(q_text.question, 'Pregnancy due date:')
        self.assertEqual(q_text.american_question, 'Pregnancy due date:')
        self.assertEqual(q_text.triggers, tuple())
        self.assertEqual(q_text.qid, 'Pregnancy_98')
        self.assertEqual(q_text.interface_element_ids, ['Pregnancy_98_0'])

        # Test rendering of form object
        form = BaseForm({
            q_text.interface_element_ids[0]: q_text.interface_elements[0]
        })
        eid = q_text.interface_element_ids[0]
        self.assertEqual(str(type(form[eid])),
                         "<class 'wtforms.fields.simple.TextAreaField'>")


class TestQuestionString(TestCase):
    def test_create(self):
        q_string = QuestionString(127, 'PetName')
        self.assertEqual(q_string.id, 127)
        self.assertEqual(q_string.group_name, 'PetName')
        self.assertEqual(q_string.set_response, None)
        self.assertEqual(q_string.response_type, 'STRING')
        self.assertEqual(q_string.question, 'Name')
        self.assertEqual(q_string.american_question, 'Name')
        self.assertEqual(q_string.triggers, tuple())
        self.assertEqual(q_string.qid, 'PetName_127')
        self.assertEqual(q_string.interface_element_ids, ['PetName_127_0'])

        # Test rendering of form object
        form = BaseForm({
            q_string.interface_element_ids[0]: q_string.interface_elements[0]
        })
        eid = q_string.interface_element_ids[0]
        self.assertEqual(str(type(form[eid])),
                         "<class 'wtforms.fields.simple.TextField'>")


class TestGroup(TestCase):
    def test_create(self):
        raise NotImplementedError()

    def test_name(self):
        raise NotImplementedError()

    def test_american_name(self):
        raise NotImplementedError()


class TestSurvey(TestCase):
    def test_create(self):
        raise NotImplementedError()

    def test_fetch_survey(self):
        raise NotImplementedError()

    def test_store_survey(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
