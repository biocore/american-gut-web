from urllib import urlencode
from json import loads

from tornado.web import HTTPError
from tornado.httpclient import HTTPClient

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.data_access.sql_connection import TRN


def _make_request(data):
    body = urlencode(data)
    client = HTTPClient()
    response = client.fetch(AMGUT_CONFIG.redcap_url, method='POST',
                            headers=None, body=body)
    if '{"error"' in response.body:
        raise HTTPError(400, loads(response.body)['error'])
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
                 LEFT JOIN ag.consents USING (redcap_record_id)
                 LEFT JOIN redcap_instruments
                    USING (redcap_instrument_id, lang)
                 WHERE redcap_record_id = %s AND redcap_instrument_id = %s;
        """
        event = TRN.execute_fetchlast(sql, [record, instrument])
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
        TRN.execute(sql, [instrument, record, event])


def get_responses(records, instrument, event):
    """Get responses for the given records

    Parameters
    ----------
    records : list of int
        records to pull information for
    instrument : str
        The instrument (survey) to get responses from
    event : int
        What event to get responses from

    Returns: list of dict of objects
        List of all matching survey responses, where each is a dictionary of
        {header: resp, ...}
    """
    data = {
        'token': AMGUT_CONFIG.redcap_token,
        'content': 'record',
        'records': ','.join(records),
        'forms': instrument,
        'events': 'event_%d_arm_1' % event,
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'label',
        'exportCheckboxLabel': 'true',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    return loads(_make_request(data))
