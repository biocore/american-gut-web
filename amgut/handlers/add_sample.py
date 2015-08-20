from wtforms import Form, SelectField, DateField, DateTimeField, TextField
from tornado.web import authenticated
from future.utils import viewitems

from amgut.connections import ag_data
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
        participant_name = self.get_argument('participant_name',
                                             'environmental')
        form = self.build_form()
        args = {k: v[0] for k, v in viewitems(self.request.arguments)}
        form.process(data=args)
        print form.data
        print args
        if not form.validate():
            self.render('add_sample.html', skid=self.current_user,
                    participant_name=participant_name,
                    form=form)
            return

        barcode = form.barcode.data
        sample_site = form.sample_site.data
        sample_date = form.sample_date.data
        sample_time = form.sample_time.data
        notes = form.notes.data

        if participant_name == 'environmental':
            # environmental sample
            env_sampled = sample_site
            sample_site = None
        else:
            env_sampled = None

        ag_login_id = ag_data.get_user_for_kit(self.current_user)

        ag_data.logParticipantSample(ag_login_id, barcode, sample_site,
                                     env_sampled, sample_date,
                                     sample_time, participant_name, notes)

        self.redirect(media_locale['SITEBASE'] + '/authed/portal/')

    @authenticated
    def get(self):
        participant_name = self.get_argument('participant_name',
                                             'environmental')
        form = self.build_form()
        self.render('add_sample.html', skid=self.current_user,
                    participant_name=participant_name,
                    form=form)

    def build_form(self):
        kit_id = self.current_user
        ag_login_id = ag_data.get_user_for_kit(kit_id)
        kit_barcodes = ag_data.getAvailableBarcodes(ag_login_id)

        form = LogSample()
        form.barcode.choices = [(v, v) for v in kit_barcodes]
        form.sample_site.choices = self._get_sample_sites()
        return form

    def _get_sample_sites(self):
        sample_site = [(v, v) for v in self._sample_sites]
        sample_site.insert(0, (0, 'Please select...'))
        return sample_site


class AddHumanSampleHandler(AddSample):
    _sample_sites = ag_data.human_sites


class AddAnimalSampleHandler(AddSample):
    _sample_sites = ag_data.animal_sites


class AddGeneralSampleHandler(AddSample):
    _sample_sites = ag_data.general_sites
