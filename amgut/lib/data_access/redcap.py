from urllib import urlencode
from json import loads

from tornado.web import HTTPError
import tornado.gen as gen
from tornado.httpclient import AsyncHTTPClient

from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.data_access.sql_connection import TRN


@gen.coroutine
def _make_request(data):
    body = urlencode(data)
    client = AsyncHTTPClient()
    response = yield client.fetch(AMGUT_CONFIG.redcap_url, method='POST',
                                  headers=None, body=body)
    # Response not always JSON, so can't always use loads
    if '{"error"' in response.body:
        raise HTTPError(400, loads(response.body)['error'])
    raise gen.Return(response.body)


def get_instrument(participant_type, language):
    """Returns the instrument name for a given participant and parameters

    participant_type : {human, animal, environmental}
        What survey type to get
    language : str
        What language the person is consented in
    """
    return "ag-%s-%s" % (participant_type, language)


@gen.coroutine
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
        'format': 'xml',
        'type': 'eav',
        'overwriteBehavior': 'normal',
        'data': info,
        'dateFormat': 'MDY',
        'returnContent': 'count',
        'returnFormat': 'json',
        'record_id': record_id
    }
    yield _make_request(data)


@gen.coroutine
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
        event_id = TRN.execute_fetchlast()
        if event_id is None:
            event_id = 1
        data = {
            'token': AMGUT_CONFIG.redcap_token,
            'content': 'surveyLink',
            'format': 'json',
            'instrument': instrument.lower().replace('-', ''),
            'event': 'event_%d_arm_1' % event_id,
            'record': record,
            'returnFormat': 'json'
        }
        yield _make_request(data)


def log_complete(record, instrument, survey_id):
    """Logs a redcap survey as completed in the database

    Parameters
    ----------
    records : list of int
        record to log for
    instrument : str
        The instrument (survey) to log for
    survey_id : str
        Survey ID for this survey
    """
    with TRN:
        event_sql = """SELECT max(redcap_event_id) + 1
                       FROM ag.ag_login_surveys
                       WHERE redcap_record_id = %s"""
        sql = """INSERT INTO ag.ag_login_surveys
                 (redcap_instrument_id, redcap_record_id, survey_id,
                  redcap_event_id)
                 (SELECT %s, %s, %s, %s
                  FROM ag.ag_login_surveys
                  WHERE redcap_record_id = %s)"""
        TRN.add(event_sql, [record])
        event_id = TRN.execute_fetchlast()
        if event_id is None:
            # First survey so nothing logged for user, default to first event
            event_id = 1
        TRN.add(sql, [instrument, record, survey_id, event_id, record])
        TRN.execute()


@gen.coroutine
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
    yield loads(_make_request(data))
