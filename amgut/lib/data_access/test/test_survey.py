from unittest import TestCase, main
from future.utils import viewitems
from wtforms.form import BaseForm
from amgut.lib.data_access.survey import (
    QuestionSingle, QuestionMultiple, QuestionText, QuestionString, Group)
# Question, Survey)


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
        self.maxDiff = None
        group = Group(1)
        self.assertEqual(group.id, 1)
        self.assertEqual(group.id_to_eid, {
            14: ['General_Information_14_0'],
            15: ['General_Information_15_0'],
            16: ['General_Information_16_0'],
            17: ['General_Information_17_0'],
            18: ['General_Information_18_0'],
            19: ['General_Information_19_0'],
            20: ['General_Information_20_0'],
            21: ['General_Information_21_0'],
            22: ['General_Information_22_0'],
            23: ['General_Information_23_0'],
            101: ['General_Information_101_0'],
            103: ['General_Information_103_0'],
            105: ['General_Information_105_0'],
            117: ['General_Information_117_0'],
            119: ['General_Information_119_0'],
            120: ['General_Information_120_0'],
            122: ['General_Information_122_0']})
        self.assertEqual(
            {k: str(type(v)) for k, v in viewitems(group.question_lookup)}, {
                14: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                15: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                16: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                17: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                18: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                19: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                20: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                21: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                22: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                23: "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
                101: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                103: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                105: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                117: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                119: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                120: "<class 'amgut.lib.data_access.survey.QuestionText'>",
                122: "<class 'amgut.lib.data_access.survey.QuestionText'>"})
        self.assertEqual([str(type(x)) for x in group.questions], [
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionSingle'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>",
            "<class 'amgut.lib.data_access.survey.QuestionText'>"])
        self.assertEqual(group.supplemental_eids, {
            'General_Information_103_0',
            'General_Information_120_0',
            'General_Information_105_0',
            'General_Information_119_0',
            'General_Information_117_0',
            'General_Information_101_0',
            'General_Information_122_0'})

    def test_name(self):
        group = Group(1)
        self.assertEqual(group.name, 'General Information')

    def test_american_name(self):
        group = Group(1)
        self.assertEqual(group.american_name, 'General Information')


class TestSurvey(TestCase):
    def test_create(self):
        raise NotImplementedError()

    def test_fetch_survey(self):
        raise NotImplementedError()

    def test_store_survey(self):
        raise NotImplementedError()


if __name__ == "__main__":
    main()
