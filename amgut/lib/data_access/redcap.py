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
    # Response not always JSON, so can't always use loads
    if '{"error"' in response.body:
        raise HTTPError(400, loads(response.body)['error'])
    return response.body


def get_instrument(participant_type, language):
    """Returns the instrument name for a given participant and parameters

    participant_type : {human, animal, environmental}
        What survey type to get
    language : str
        What language the person is consented in
    """
    return "ag-%s-%s" % (participant_type, language)


def create_record(record_id, ag_login_id, participant_name):
    """Creates a new record on redcap for the participant

    Parameters
    ----------
    record_id : int
        record ID to add
    ag_login_id : UUID4
        Login ID to associate the record with
    participant_name : str
        participant name to associate the record with
    """
    info = '''<?xml version="1.0" encoding="UTF-8" ?>
    <records>
       <item>
          <record>%(record)d</record>
          <field_name>ag_login_id</field_name>
          <value>%(login)s</value>
          <redcap_event_name>event_1_arm_1</redcap_event_name>
       </item>
       <item>
          <record>%(record)d</record>
          <field_name>participant_name</field_name>
          <value>%(name)s</value>
          <redcap_event_name>event_1_arm_1</redcap_event_name>
       </item>
    </records>''' % {'record': record_id, 'login': ag_login_id,
                     'name': participant_name}
    data = {
        'token': AMGUT_CONFIG.redcap_token,
        'content': 'record',
        'format': 'json',
        'type': 'eav',
        'overwriteBehavior': 'normal',
        'data': info,
        'dateFormat': 'MDY',
        'returnContent': 'count',
        'returnFormat': 'json',
        'record_id': record_id
    }
    return _make_request(data)


def get_survey_url(record, instrument='ag-human-en-US'):
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
            'instrument': instrument.lower().replace('-', ''),
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

    Returns: list of dict of objects
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
