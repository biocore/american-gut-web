#!/usr/bin/env python

from datetime import datetime

from data_access_connections import data_access_factory
from enums import ServerConfig, DataAccessType

from amgut import db_conn

data_access = data_access_factory(ServerConfig.data_access_type,
                                  'qiime')


COUNTRIES_SQL = """select country from iso_country_lookup"""
COUNTRIES = {x[0] for x in db_conn.execute_fetchall(COUNTRIES_SQL)}


OLD_COUNTRIES = data_access.getControlledVocabValueList(28)
for code, country in OLD_COUNTRIES.items():
    if country == 'USA':
        OLD_COUNTRIES[code] = 'United States'
    elif country == "Cote d'Ivoire":
        OLD_COUNTRIES[code] = "Cote D'ivoire"
    elif country == 'Iran':
        OLD_COUNTRIES[code] = 'Iran, Islamic Republic of'
    elif country == 'Syria':
        OLD_COUNTRIES[code] = 'Syrian Arab Republic'
    elif country == 'Russia':
        OLD_COUNTRIES[code] = 'Russian Federation'
    elif country == 'Taiwan':
        OLD_COUNTRIES[code] = 'Taiwan, Province of China'
    elif country == 'South Korea':
        OLD_COUNTRIES[code] = 'Korea, Republic of'


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

    return {iname: ival for iname, ival in db_conn.execute_fetchall(sql)
            if ival is not None}


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
    bool or str
        If the user is not an old participant, returns False; otherwise,
        returns the one survey_id associated with the participant
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

    return survey_id


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
        new[108] = int(round(height_cm or 2.54*height_in))
        new[109] = 'centimeters'

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
        new[36] = 'No'

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

    return new


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
    new[103] = old['race_other'] or ''
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
    new[116] = old['about_yourself_text'] or ''
    return new


def exercise_frequency(old, new):
    new_val = _frequency(old['exercise_frequency'])

    if new_val is not None:
        new[24] = new_val

    return new


def zip_code(old, new):
    new[115] = old['zip_code'] or ''
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
    elif old_val == 'no':
        new[49] = 'No'

    return new


def weight_change(old, new):
    old_val = old['weight_change'] 
    if old_val is not None:
        new[43] = old_val

    return new


def supplements(old, new, ag_login_id, pname):
    old_val = old['supplements'] 

    if old_val is None:
        return new

    new_val = old_val.capitalize()
    new[6] = new_val

    if new_val == 'Yes':
        # Fill in responses for 104
        responses = get_multiples(ag_login_id, pname, 'supplements_fields')
        responses = '; '.join([v for k, v in responses.items()])
        new[104] = responses

    return new


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
        new[124] = '; '.join(meds)

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


def conditions_medication(old, new, ag_login_id, pname):
    old_val = old['conditions_medication']
    if old_val is None:
        return new

    new_val = old_val.capitalize()
    new[49] = new_val

    if new_val == 'Yes':
        responses = get_multiples(ag_login_id, pname, 'generalmeds')
        # Safe to include new[99] here since this function is executed after
        # the other that affects new[99]
        responses = '; '.join([new[99]] + [v for k, v in responses.items()])

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
    new[126] = old['antibiotic_condition'] or ''
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
        if old_val == 'Omnivore but no red meat':
            new[1] = 'Omnivore but do not eat red meat'
        else:
            new[1] = old_val

    return new


def pool_frequency(old, new):
    new_val = _frequency(old['pool_frequency'])

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
    old_val = old['exercise_location']

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
    if 'or antiperspirant' in old_val:
        old_val = old_val.replace('or antiperspirant', 'or an antiperspirant')

    new[34] = old_val

    return new


def country_of_birth(old, new):
    old_val = old['country_of_birth']
    if old_val is not None:
        old_val = int(old_val)
        new[110] = OLD_COUNTRIES[old_val]

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
        new[113] = int(round(weight_kg or 2.20462*weight_lbs))
        new[114] = 'kilograms'

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
    new[98] = old['pregnant_due_date'] or ''
    return new


def diabetes(old, new):
    old_val = old['diabetes']
    if old_val is None:
        return new

    if old_val == 'I do not have diabetes':
        new[82] = 'I do not have this condition'

    return new


def last_travel(old, new):
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
        # %B gets the locale's full name for the month
        # %Y gets the 4-digit year
        new[111] = d.strftime('%B')
        new[112] = d.strftime('%Y')
    except ValueError:
        return new

    return new

# Each of the functions above takes the old survey responses and the new
# survey responses, and returns a copy of the new survey responses with
# modifications made based on the old survey responses


if __name__ == '__main__':
    # Set up defaults for new questions
    # If it's a single or multiple, then default is "Unspecified"
    # If it's a string or text, then the default is ''
    sql = """select survey_question_id, survey_response_type
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

    total_surveys = 0
    transfers = 0
    for row in old_surveys():
        total_surveys += 1
        ag_login_id = row.pop('ag_login_id')
        pname = row.pop('participant_name')

        survey_id = verify_old_participant(ag_login_id, pname)
        if not survey_id:
            continue
        transfers += 1

        # record the new responses, which begin as default values based on
        # response type
        new_responses = {
            qid: default_values[response_type]
            for qid, response_type in qids_response_types.items()}

        new_responses = pku(row, new_responses)
        new_responses = height(row, new_responses)
        new_responses = drinking_water_source(row, new_responses)
        new_responses = asthma(row, new_responses)
        new_responses = current_residence_duration(row, new_responses)
        new_responses = nonfoodallergies(row, new_responses)
        new_responses = livingwith(row, new_responses)
        new_responses = softener(row, new_responses)
        new_responses = skin_condition(row, new_responses)
        new_responses = migraine(row, new_responses)
        new_responses = flu_vaccine_date(row, new_responses)
        new_responses = pregnant(row, new_responses)
        new_responses = gender(row, new_responses)
        new_responses = csection(row, new_responses)
        new_responses = race(row, new_responses)
        new_responses = cosmetics_frequency(row, new_responses)
        new_responses = special_restrictions(row, new_responses, ag_login_id, pname)
        new_responses = race_other(row, new_responses)
        new_responses = ibd(row, new_responses)
        new_responses = foodallergies_other(row, new_responses)
        new_responses = sleep_duration(row, new_responses)
        new_responses = about_yourself_text(row, new_responses)
        new_responses = exercise_frequency(row, new_responses)
        new_responses = zip_code(row, new_responses)
        new_responses = nails(row, new_responses)
        new_responses = diabetes_medication(row, new_responses, ag_login_id, pname)
        new_responses = weight_change(row, new_responses)
        new_responses = supplements(row, new_responses, ag_login_id, pname)
        new_responses = antibiotic_select(row, new_responses, ag_login_id, pname)
        new_responses = foodallergies(row, new_responses)
        new_responses = acne_medication(row, new_responses)
        new_responses = acne_medication_otc(row, new_responses)
        new_responses = conditions_medication(row, new_responses, ag_login_id, pname)
        new_responses = gluten(row, new_responses)
        new_responses = smoking_frequency(row, new_responses)
        new_responses = contraceptive(row, new_responses)
        new_responses = antibiotic_condition(row, new_responses)
        new_responses = cat(row, new_responses)
        new_responses = diet_type(row, new_responses)
        new_responses = pool_frequency(row, new_responses)
        new_responses = alcohol_frequency(row, new_responses)
        new_responses = seasonal_allergies(row, new_responses)
        new_responses = exercise_location(row, new_responses)
        new_responses = tonsils_removed(row, new_responses)
        new_responses = deodorant_use(row, new_responses)
        new_responses = country_of_birth(row, new_responses)
        new_responses = teethbrushing_frequency(row, new_responses)
        new_responses = chickenpox(row, new_responses)
        new_responses = weight(row, new_responses)
        new_responses = appendix_removed(row, new_responses)
        new_responses = flossing_frequency(row, new_responses)
        new_responses = hand(row, new_responses)
        new_responses = pregnant_due_date(row, new_responses)
        new_responses = diabetes(row, new_responses)
        new_responses = last_travel(row, new_responses)
        new_responses = lactose(row, new_responses)
        new_responses = dog(row, new_responses)
        new_responses = roommates(row, new_responses)
        new_responses = multivitamin(row, new_responses)
        new_responses = birth_date(row, new_responses)

        sql = """insert into {}
                 (survey_id, survey_question_id, response)
                 VALUES 
                 (%s, %s, %s)"""

        with db_conn.get_postgres_cursor() as cur:
            for qid, response_type in qids_response_types.items():
                if response_type == 'SINGLE':
                    query = sql.format('survey_answers')
                    cur.execute(query, (survey_id, qid, new_responses[qid]))
                elif response_type == 'MULTIPLE':
                    query = sql.format('survey_answers')
                    # If we have a response other than the default response, then
                    # pop the default value
                    if len(new_responses[qid]) > 1:
                        assert(new_responses[qid][0] == 'Unspecified')
                        new_responses[qid].pop(0)

                    # Record all remaining responses to the database
                    for resp in new_responses[qid]:
                        cur.execute(query, (survey_id, qid, resp))

                elif response_type in ('STRING', 'TEXT'):
                    response = '["%s"]' % new_responses[qid]
                    query = sql.format('survey_answers_other')
                    cur.execute(query, (survey_id, qid, response))
                else:
                    raise ValueError("Unrecognized response type: %s" %
                                     response_type)

    print "transferred", transfers, "out of", total_surveys, "attempts"

