#!/usr/bin/env python

from datetime import datetime

from amgut import db_conn
import binascii


COUNTRIES_SQL = """select country from iso_country_lookup"""
COUNTRIES = {x[0] for x in db_conn.execute_fetchall(COUNTRIES_SQL)}


def old_surveys():
    """Get all old surveys as a list of dicts keyed by column name
    """
    sql = """select * from ag_human_survey"""

    with db_conn.get_postgres_cursor() as cur:
        cur.execute(sql)
        columns = [x[0] for x in cur.description]

        rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    return rows


def get_multiples(ag_login_id, pname, prefix):
    """Gets multiples answers from the ag_survey_multiples table

    Parameters
    ----------
    ag_login_id : str
    pname : str
        the name of the participant that provided the answer
    prefix : str
        the prefix of the question (e.g., "diabetes_medications" would retrieve
        "diabetes_medications_1", "diabetes_medications_2", etc.

    Returns
    -------
    list
        A list of the item values
    """
    sql = """select item_name, item_value from ag_survey_multiples
             where item_name like '{}%'
             and ag_login_id = '{}'
             and participant_name = '{}'""".format(prefix, ag_login_id, pname)

    return {iname: ival for iname, ival in db_conn.execute_fetchall(sql)}


def verify_old_participant(ag_login_id, pname):
    """Checks if an (ag_login_id, pname) tuple represents an old survey or not

    Old participants can be identified because they will have an entry in
    the ag_consent table, but answers in neither the survey_answers table nor
    the survey_answers_other table

    Parameters
    ----------
    ag_login_id : str
        The ag_login_id of the user
    pname : str
        The name of the participant

    Returns
    -------
    bool
        True if the user is an old participant, False if not
    """
    survey_ids_sql = """select survey_id from ag_login_surveys
                        where ag_login_id = %s and participant_name = %s"""
     
    surveys = db_conn.execute_fetchall(survey_ids_sql, (ag_login_id, pname))

    # There should be only one survey, since at the time of the writing of
    # this script, we did not support multiple surveys per participant. So,
    # this is more of a sanity check at this point
    if len(surveys) != 1:
        print ("More than one survey detected for (%s, %s)" %
               (ag_login_id, pname))
        return False
    else:
        survey_id = surveys[0][0]

    # Checks if there are entries in the survey_answers table
    answers_sql = """select exists(select * from survey_answers
                     where survey_id = %s)"""

    # Checks if there are entries in the survey_answers_other table
    answers_other_sql = """select exists(select * from survey_answers_other
                           where survey_id = %s)"""
    
    answers = db_conn.execute_fetchone(answers_sql, [survey_id])[0]
    if answers:
        print "%s (%s, %s) already has answers" % (survey_id, ag_login_id,
                                                   pname)
        return False

    answers_other = db_conn.execute_fetchone(answers_other_sql, [survey_id])[0]
    if answers_other:
        print "%s (%s, %s) already has answers_other" % (survey_id,
                                                         ag_login_id, pname)
        return False

    return True


def _medical(old_response):
    """For the medical questions, we can only say unspecified, or no

    Parameters
    ----------
    old_response : 'on' or None
        If the box was checked in the original survey, it will be 'on';
        otherwise it will be None
    """
    if old_response is None:
        return None

    old_response = old_response.lower()
    if old_response == 'no':
        return 'I do not have this condition'
    else:
        return None


def _frequency(old_val):
    """There is a subtle change in the responses for the frequency questions

    The old "Rarely (few times/month)" has become "Rarely (a few times/month)"
    """
    if old_val is None:
        return None

    if old_val.startswith('Rarely'):
        return 'Rarely (a few times/month)'
    else:
        return old_val


_float = lambda x: None if x is None else float(x)


def pku(old, new):
    new_val = _medical(old['pku'])
    if new_val is not None:
        new[94] = new_val

    return new


def height(old, new):
    height_in = _float(old['height_in'])
    height_cm = _float(old['height_cm'])

    if height_in is not None or height_cm is not None:
        # If we have a value for both units of measurement, go with the cm
        # response. If we have only inches, convert to cm
        new[108] = height_cm or 2.54*height_in

    return new


def drinking_water_source(old, new):
    old_val = old['drinking_water_source'] 
    if old_val is not None:
        new[13] = old_val

    return new


def asthma(old, new):
    new_val = _medical(old['asthma'])
    if new_val is not None:
        new[93] = new_val

    return new


def current_residence_duration(old, new):
    # This question has changed from "your current residence" to "your current
    # STATE of residence", so we can't use the old response
    return new


def nonfoodallergies(old, new):
    # old responses:
    # --------------
    # dander
    # sun
    # drug
    # beestings
    # poisonivy
    # no

    # The checkboxes for this question are either "on" or None

    # TODO: cannot proceed here until we resolve #325; we have no way of
    # recording "No, I do not have any allergies" on the new survey

    # t = 'survey_answers'
    # rows = []

    # dander = row['nonfoodallergies_dander']
    # sun = row['nonfoodallergies_sun']
    # drug = row['nonfoodallergies_drug']
    # beestings = row['nonfoodallergies_beestings']
    # poisonivy = row['nonfoodallergies_poisonivy']
    # dander = row['nonfoodallergies_dander']
    return new


def livingwith(old, new):
    old_val = old['livingwith']
    if old_val is None:
        return new

    old_val = old_val.lower()
    if old_val == 'not_sure':
        new[19] = 'Not sure'
    elif old_val == 'yes':
        new[19] = 'Yes'
    elif old_val == 'no':
        new[19] = 'No'

    return new


def softener(old, new):
    old_val = old['softener']
    if old_val is None:
        return new

    old_val = old_val.lower()
    if old_val == 'yes':
        new[36] = 'Yes'
    if old_val == 'no':
        new[36] == 'No'

    return new


def skin_condition(old, new):
    old_val = old['skin_condition']

    if old_val is None:
        return new

    if old_val == 'I do not have a skin condition':
        new[88] = 'I do not have this condition'

    return new


def migraine(old, new):
    new_val = _medical(old['migraine'])
    if new_val is not None:
        new[92] = new_val

    return new


def flu_vaccine_date(old, new):
    old_val = old['flu_vaccine_date']
    if old_val is None:
        return new

    if old_val == 'In the past week':
        new[40] = 'Week'
    elif old_val == 'In the past month':
        new[40] = 'Month'
    elif old_val == 'In the past 6 months':
        new[40] = '6 months'
    elif old_val == 'In the past year':
        new[40] = 'Year'
    elif old_val == 'Not in the last year':
        new[40] = 'I have not gotten the flu vaccine in the past year.'

    return new


def pregnant(old, new):
    old_val = old['pregnant']
    if old_val is None:
        return new

    old_val = old_val.lower()
    if old_val == 'no':
        new[42] = 'No'
    if old_val == 'yes':
        new[42] = 'Yes'
    if old_val == 'notsure':
        new[42] = 'Not sure'

    return row


def gender(old, new):
    if old['gender'] is not None:
        new[107] = old['gender']

    return new


def csection(old, new):
    old_val = old['csection']
    if old_val is None:
        return new

    old_val = old_val.lower()
    if old_val == 'yes':
        new[50] = 'Yes'
    if old_val == 'no':
        new[50] = 'No'
    if old_val == 'not_sure':
        new[50] = 'Not sure'

    return new


def race(old, new):
    old_val = old['race']
    if old_val is not None:
        new[14] = old_val

    return new


def cosmetics_frequency(old, new):
    new_val = _frequency(old['cosmetics_frequency'])

    if new_val is not None:
        new[33] = new_val

    return new


def special_restrictions(old, new, ag_login_id, pname):
    old_val = old['special_restrictions']
    if old_val is not None:
        new_val = old_val.capitalize()
        new[12] = new_val
        if new_val == 'Yes':
            # this triggers 118
            restrictions = get_multiples(ag_login_id, pname,
                                         'dietrestrictions')
            restrictions = [v for k, v in restrictions.items()]
            new[118] = '; '.join(restrictions)

    return new

def race_other(old, new):
    new[103] = old['race_other']
    return new


def ibd(old, new):
    old_val = old['ibd']
    if old_val is None:
        return new

    if old_val == 'I do not have IBD':
        new[83] = 'I do not have this condition'

    return new


def foodallergies_other(old, new):
    # There is no supplement for this question in the survey. Maybe there
    # should be?  See github.com/biocore/american-gut-web/issues/326
    return new


def sleep_duration(old, new):
    old_val = old['sleep_duration']
    if old_val is not None:
        new[35] = old_val

    return new


def about_yourself_text(old, new):
    new[116] = old['about_yourself_text']
    return new


def exercise_frequency(old, new):
    new_val = _frequency(old['exercise_frequency'])

    if new_val is not None:
        new[24] = new_val

    return new


def zip_code(old, new):
    new[115] = old['zip_code']
    return new


def nails(old, new):
    old_val = old['nails']
    if old_val is not None:
        new[26] = old_val.capitalize()

    return new


def diabetes_medication(old, new, ag_login_id, pname):
    # there is no new question specifically about diabetes medication, but
    # there is a general questiona to the effect of "Do you take any OTC or
    # prescription medications for conditions other than facial acne?"
    # so we'll activate that question (give it a Yes) and also insert them
    # into the free-entry text box
    old_val = old['diabetes_medication']
    if old_val == 'yes':
        meds = get_multiples(ag_login_id, pname, 'diabetes_medications')
        meds = [v for k, v in meds.items()]
        new[49] = 'Yes'
        new[99] = '; '.join(meds)
    elif old_val == 'no'
        new[49] = 'No'

    return new


def weight_change(old, new):
    old_val = old['weight_change'] 
    if old_val is not None:
        new[43] = old_val

    return new


def supplements(row):
    # TODO: Not sure what to do here since we can map the supplements question
    # but the triggering question has changed...
    return row


def antibiotic_select(old, new, ag_login_id, pname):
    old_val = old['antibiotic_select']
    if old_val is None:
        return new

    trigger = False
    if old_val == 'In the past week':
        new[39] = 'Week'
        trigger = True
    elif old_val == 'In the past month':
        new[39] = 'Month'
        trigger = True
    elif old_val == 'In the past 6 months':
        new[39] = '6 months'
        trigger = True
    elif old_val == 'In the past year':
        new[39] = 'Year'
    elif old_val == 'Not in the last year':
        new[39] = 'I have not taken antibiotics in the past year.'

    if trigger:
        meds = get_multiples(ag_login_id, pname, 'antibiotic_med')
        meds = [v for k, v in meds.items()]
        new[126] = '; '.join(meds)

    return new


def foodallergies(old, new):
    #9
    # old_responses:
    # --------------
    # treenuts
    # shellfish
    # peanuts
    # other
    # other_text

    # The checkboxes for this question are either "on" or None

    # TODO: cannot proceed here until we resolve #325; we have no way of
    # recording "No, I do not have any allergies" on the new survey

    return new


def acne_medication(old, new):
    old_val = old['acne_medication']
    if old_val is not None:
        new[47] = old_val.capitalize()

    return new


def acne_medication_otc(old, new):
    old_val = old['acne_medication_otc']
    if old_val is not None:
        new[48] = old_val.capitalize()

    return new


def conditions_medication(old, new):
    old_val = old['conditions_medication']
    if old_val is not None:
        new[49] = old_val.capitalize()

    return new


def gluten(old, new):
    old_val = old['gluten']
    if old_val is not None:
        new_val = old_val.capitalize()
        if new_val == 'No':
            new[8] = 'No'

    return new


def smoking_frequency(old, new):
    new_val = _frequency(old['smoking_frequency'])

    if new_val is not None:
        new[28] = new_val

    return new


def contraceptive(old, new):
    old_val = old['contraceptive']
    if old_val is None:
        return new

    if old_val == 'No':
        new[41] = 'No'
    elif old_val.startswith('I take the'):
        new[41] = 'Yes, I am taking the "pill"'
    elif old_val == 'I use an injected contraceptive (DMPA)':
        new[41] = 'Yes, I use an injected contraceptive (DMPA)'
    elif old_val == 'I use the NuvaRing':
        new[41] = 'Yes, I use the NuvaRing'
    elif old_val == 'I use a contraceptive patch (Ortho-Evra)':
        new[41] = 'Yes, I use a contraceptive patch (Ortho-Evra)'

    return new


def antibiotic_condition(old, new):
    new[124] = old['antibiotic_condition']
    return new


def cat(old, new):
    old_val = old['cat']
    if old_val is not None:
        new[21] = old_val.capitalize()

    return new


def diet_type(old, new):
    old_val = old['diet_type']

    if old_val is not None:
        # Only one subtle wording change here
        if old_val == 'Omnivore but no read meat':
            new[1] = 'Omnivore but do not eat red meat'
        else:
            new[1] = old_val

    return new


def pool_frequency(old, new):
    new_val = _frequency(old['pool_freqeuncy'])

    if new_val is not None:
        new[27] = new_val

    return new


def alcohol_frequency(old, new):
    new_val = _frequency(old['alcohol_frequency'])

    if new_val is not None:
        new[29] = new_val

    return new


def seasonal_allergies(old, new):
    old_val = old['seasonal_allergies']

    if old_val is not None:
        new[53] = old_val.capitalize()

    return new


def exercise_location(old, new):
    old_val = old['seasonal_allergies']

    if old_val is not None:
        new[25] = old_val

    return new


def tonsils_removed(old, new):
    old_val = old['tonsils_removed']

    if old_val is not None:
        new[44] = old_val.capitalize()

    return new


def deodorant_use(old, new):
    old_val = old['deoderant_use']
    if old_val is None:
        return new
    
    if 'deoderant' in old_val:
        old_val = old_val.replace('deoderant', 'deodorant')

    new[34] = old_val

    return new


def country_of_birth(old, new):
    # TODO: convert the numerical values in the old table to the countries
    # in the new database
    return new


def teethbrushing_frequency(old, new):
    new_val = _frequency(old['teethbrushing_frequency'])

    if new_val is not None:
        new[31] = new_val

    return new


def chickenpox(old, new):
    old_val = old['chickenpox']

    if old_val is not None:
        new[46] = old_val.capitalize()

    return new


def weight(old, new):
    weight_lbs = _float(old['weight_lbs'])
    weight_kg = _float(old['weight_kg'])

    if weight_lbs is not None or weight_kg is not None:
        # If we have a value for both units of measurement, go with the kg
        # response. If we have only lbs, convert to kg
        new[113] = weight_kg or 2.20462*weight_lbs

    return new


def appendix_removed(old, new):
    old_val = old['appendix_removed']

    if old_val is not None:
        new[45] = old_val.capitalize()

    return new


def flossing_frequency(old, new):
    new_val = _frequency(old['flossing_frequency'])

    if new_val is not None:
        new[32] = new_val

    return new


def hand(old, new):
    old_val = old['hand']
    if old_val is None:
        return new

    if old_val == 'left':
        new[22] = 'I am left handed'
    elif old_val == 'right':
        new[22] = 'I am right handed'
    elif old_val == 'ambidextrous':
        new[22] = 'I am ambidextrous'

    return new


def pregnant_due_date(old, new):
    new[98] = old['pregnant_due_date']
    return new


def diabetes(old, new):
    old_val = old['diabetes']
    if old_val is None:
        return new

    if old_val == 'I do not have diabetes':
        new[82] = 'I do not have this condition'

    return new


def last_travel(row):
    old_val = old['last_travel']

    if old_val is None:
        return new

    if old_val == 'Within the past month':
        new[16] = 'Month'
    elif old_val == 'Within the past 3 months':
        new[16] = '3 months'
    elif old_val == 'Within the past 6 months':
        new[16] = '6 months'
    elif old_val == 'Within the past year':
        new[16] = '1 year'
    elif old_val in ('More than one year ago', 'Never'):
        new[16] = 'I have not been outside of my country of residence in the past year.'

    return new


def lactose(old, new):
    old_val = old['lactose']

    if old_val is not None:
        new[7] = old_val.capitalize()

    return new


def dog(old, new):
    old_val = old['dog']

    if old_val is not None:
        new[20] = old_val.capitalize()

    return new


def roommates(old, new):
    old_val = old['roommates']

    if old_val is not None:
        new[17] = old_val

    return new


def multivitamin(old, new):
    old_val = old['multivitamin']

    if old_val is not None:
        new[2] = old_val.capitalize()

    return new


def birth_date(old, new):
    old_val = old['birth_date']
    if old_val is None:
        return new

    try:
        d = datetime.strptime(old_val, '%m/%d/%Y')
    except ValueError:
        return new

    # %B gets the locale's full name for the month
    # %Y gets the 4-digit year
    new[111] = d.strftime('%B')
    new[112] = d.strftime('%Y')

    return new

# Each of the functions above takes the old survey responses and the new
# survey responses, and returns a copy of the new survey responses with
# modifications made based on the old survey responses


if __name__ == '__main__':
    # Set up defaults for new questions
    # If it's a single or multiple, then default is "Unspecified"
    # If it's a string or text, then the default is ''
    sql = """select survey_question_id, response_type
             from survey_question_response_type"""

    # maps question IDs to response types
    qids_response_types = {row[0]: row[1]
                           for row in db_conn.execute_fetchall(sql)}

    # maps response types to default values. Using lists so that the insert
    # later can be agnostic of the type of data being inserted
    default_values = {'SINGLE': 'Unspecified',
                      'MULTIPLE': ['Unspecified'],
                      'STRING': '',
                      'TEXT': ''}

    for row in old_surveys():
        ag_login_id = row.pop('ag_login_id')
        pname = row.pop('participant_name')

        if not verify_old_participant(ag_login_id, pname):
            continue

        # Generate a new survey ID for this participant
        survey_id = binascii.hexlify(os.urandom(8))

        # record the new responses, which begin as default values based on
        # response type
        new_responses = {}
            qid: default_values[response_type]
            for qid, response_type in qids_response_types.items()}

        # TODO: execute all relevant functions above on the row, then insert
        # into the appropriate tables (depending on response type)

        sql = """insert into {}
                 (survey_id, survey_question_id, response)
                 VALUES 
                 (%s, %s, %s)"""

        for qid, response_type in qids_response_types.items():
            if response_type == 'SINGLE':
                query = sql.format('survey_answers')
                db_conn.execute(query, (survey_id, qid, new_responses[qid]))
            elif response_type == 'MULTIPLE':
                query = sql.format('survey_answers')
                # If we have a response other than the default response, then
                # pop the default value
                if len(new_responses[qid]) > 1:
                    new_responses[qid].pop(0)

                # Record all remaining responses to the database
                for resp in new_responses[qid]:
                    db_conn.execute(query, (survey_id, qid, resp))

            elif response_type in ('STRING', 'TEXT'):
                query = sql.format('survey_answers_other')
                db_conn.execute(query, (survey_id, qid, new_responses[qid]))
            else:
                raise ValueError("Unrecognized response type: %s" %
                                 response_type)

