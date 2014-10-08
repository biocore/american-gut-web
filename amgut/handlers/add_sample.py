from wtforms import Form, SelectField, DateField, DateTimeField, TextField
from tornado.web import authenticated

from amgut.util import AG_DATA_ACCESS
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


class LogSample(Form):
    barcode = SelectField()
    sample_site = SelectField()
    sample_date = DateField(format='%m/%d/%Y')
    sample_time = DateTimeField(format='%I:%M %p')
    notes = TextField('notes')


class AddSample(BaseHandler):
    _sample_sites = []

    @authenticated
    def post(self):
        # Required vars
        barcode = self.get_argument('barcode')
        sample_date = self.get_argument('sample_date')
        sample_time = self.get_argument('sample_time')
        notes = self.get_argument('notes')
        participant_name = self.get_argument('participant_name')
        sample_site = self.get_argument('sample_site', '')

        if participant_name == 'environmental':
            # environmental sample
            env_sampled = sample_site
            sample_site = None
        else:
            env_sampled = None

        ag_login_id = AG_DATA_ACCESS.get_user_for_kit(self.current_user)

        AG_DATA_ACCESS.logParticipantSample(ag_login_id, barcode, sample_site,
                                            env_sampled, sample_date,
                                            sample_time, participant_name,
                                            notes)

        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')

    @authenticated
    def get(self):
        kit_id = self.current_user
        ag_login_id = AG_DATA_ACCESS.get_user_for_kit(kit_id)
        kit_barcodes = AG_DATA_ACCESS.getAvailableBarcodes(ag_login_id)
        participant_name = self.get_argument('participant_name',
                                             'environmental')

        form = LogSample()
        form.barcode.choices = [(v, v) for v in kit_barcodes]
        form.sample_site.choices = self._get_sample_sites()

        self.render('add_sample.html', skid=kit_id,
                    kit_barcodes=kit_barcodes,
                    participant_name=participant_name,
                    form=form)

    def _get_sample_sites(self):
        sample_site = [(v, v) for v in self._sample_sites]
        sample_site.insert(0, (0, 'Please select...'))
        return sample_site


class AddHumanSampleHandler(AddSample):
    _sample_sites = AG_DATA_ACCESS.human_sites


class AddAnimalSampleHandler(AddSample):
    _sample_sites = AG_DATA_ACCESS.animal_sites


class AddGeneralSampleHandler(AddSample):
    _sample_sites = AG_DATA_ACCESS.general_sites
