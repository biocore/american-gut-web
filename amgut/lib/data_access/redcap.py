from urllib import urlencode
from json import loads

from tornado.web import HTTPError
from tornado.httpclient import HTTPClient

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.data_access.sql_connection import TRN


# Explanation of redcap and interactions with it:
# Redcap has three layers of IDs: record_id, survey_id, and event_id.

# record_id is the id given to a single person in the redcap system, analagous
# to the host_subject_id.

# survey_id is the name of the survey the person will be taking.

# event_id is the id of the single time a person has taken the survey. It
# counts up from 1 for each person in each survey. These must be manually
# created for each survey before the survey is used, so we don't want to waste
# any if a person starts a survey and does not finish and log it.

# Examples - all examples use a tuple of (record_id, survey_id, event_id) and
# are ordered sequentially. Making redcap calls in this order produces a valid
# survey database state.

# (1, 'ag-human-en-US', 1) = User 1 just took the US english human survey for
# the first time.
# (1, 'ag-human-en-US', 2) = User 1 just took the US english human survey for
# the second time.
# (2, 'ag-human-en-US', 1) = User 2 just took the US english human survey for
# the first time.
# (1, 'ag-animal-en-US', 1) = User 1 just took the US english pet survey for
# the first time.
# (1, 'ag-human-fr-CA', 1) = User 1 just took the Canadian french human survey
# for the first time.
# (1, 'ag-human-fr-CA', 2) = User 1 just took the Canadian french human survey
# for the second time.
# (3, 'ag-human-fr-CA', 1) = User 3 just took the Canadian french human survey
# for the first time.

# From these examples, you can see that the event ID is tied to the survey and
# record ID, with event_id starting at 1 for each record for each survey.

def _make_request(data):
    body = urlencode(data)
    client = HTTPClient()
    response = client.fetch(AMGUT_CONFIG.redcap_url, method='POST',
                            headers=None, body=body)
    # Response not always JSON, so can't always use loads. Error messages,
    # however, are always JSON and are the only thing that have the error key.
    try:
        error = loads(response.body)['error']
    except (KeyError, ValueError):
        # Return JSON doesn't have error key, so valid, or return is a regualar
        # non-JSON string, so valid
        pass
    else:
        raise HTTPError(400, error)
    return response.body


def get_survey_url(record, instrument='ag_human_en_us'):
    """Genereates a new survey link for a given record

    Parameters
    ----------
    record : int
        Redcap record (consent) to attach this survey to
    instrument : str, optional
        The instrument (survey) to get the URL for. Default ag_human_en_us

    Returns
    -------
    str
        URL for the survey
    """
    with TRN:
        # Get the event ID for the survey, or 1 if first survey
        sql = """SELECT MAX(redcap_event_id) + 1
                 FROM ag.ag_login_surveys
                 LEFT JOIN ag.ag_consent USING (redcap_record_id)
                 LEFT JOIN redcap_instruments
                    USING (redcap_instrument_id, lang)
                 WHERE redcap_record_id = %s AND redcap_instrument_id = %s;
        """
        TRN.add(sql, [record, instrument])
        event = TRN.execute_fetchlast()
        if event is None:
            event = 1
        data = {
            'token': AMGUT_CONFIG.redcap_token,
            'content': 'surveyLink',
            'format': 'json',
            'instrument': 'ag_human',
            'event': 'event_%d_arm_1' % event,
            'record': record,
            'returnFormat': 'json'
        }
        return _make_request(data)


def log_complete(record, instrument, event):
    """Logs a redcap survey as completed in the database

    Parameters
    ----------
    records : list of int
        record to log for
    instrument : str
        The instrument (survey) to log for
    event : int
        Event to log for
    """
    with TRN:
        sql = """INSERT INTO ag.ag_login_surveys
                 (redcap_instrument_id, redcap_record_id,
                  redcap_event_id)
                 VALUES (%s, %s, %s)"""
        TRN.add(sql, [instrument, record, event])
        TRN.execute()


def get_responses(records, instrument, event=None):
    """Get responses for the given records

    Parameters
    ----------
    records : list of int
        records to pull information for
    instrument : str
        The instrument (survey) to get responses from
    event : int, optional
        What event to get responses from. Default all

    Returns
    -------
    list of dict of objects
        List of all matching survey responses, where each is a dictionary of
        {header: resp, ...}
    """
    data = {
        'token': AMGUT_CONFIG.redcap_token,
        'content': 'record',
        'records': ','.join(map(str, records)),
        'forms': instrument,
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'label',
        'exportCheckboxLabel': 'true',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    if event is not None:
        data['events'] = 'event_%d_arm_1' % event,
    return loads(_make_request(data))
