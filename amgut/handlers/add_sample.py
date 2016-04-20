from datetime import datetime
from wtforms import (Form, SelectField, DateField, DateTimeField, TextField,
                     HiddenField, validators)
from tornado.web import authenticated
from future.utils import viewitems

from amgut.connections import ag_data
from amgut.lib.constants import human_sites, animal_sites, general_sites
from amgut.handlers.base_handlers import BaseHandler
from amgut import media_locale


class LogSample(Form):
    required = validators.required
    participant_name = HiddenField(u'participant_name')
    barcode = SelectField(validators=[required("Required field")])
    sample_site = SelectField(validators=[required("Required field")])
    sample_date = DateField(validators=[required("Required field")],
                            format='%m/%d/%Y')
    sample_time = DateTimeField(validators=[required("Required field")],
                                format='%I:%M %p')
    notes = TextField('notes')


class AddSample(BaseHandler):
    _sample_sites = []
    page_type = ''

    @authenticated
    def post(self):
        # Required vars
        participant_name = self.get_argument('participant_name',
                                             'environmental')
        form = self.build_form()
        args = {a: v[0] for a, v in viewitems(self.request.arguments)}
        form.process(data=args)
        # Validate input
        invalid = False
        if not form.validate():
            invalid = True
        else:
            try:
                datetime.strptime(form.sample_date.data, '%m/%d/%Y').date()
            except ValueError:
                invalid = True
                form.sample_date.errors = ['Invalid date format']
            try:
                datetime.strptime(form.sample_time.data, '%I:%M %p').time()
            except ValueError:
                invalid = True
                form.sample_time.errors = ['Invalid time format']
        if invalid:
            self.render('add_sample.html', skid=self.current_user,
                        participant_name=participant_name,
                        form=self.build_form(), page_type=self.page_type,
                        message='Invalid form submission, please try again')
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
        participant_name = self.get_argument('participant_name', None)
        if participant_name is None:
            self.redirect('/authed/add_sample_overview/')
        form = self.build_form()
        self.render('add_sample.html', skid=self.current_user,
                    participant_name=participant_name,
                    form=form, page_type=self.page_type, message='')

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
    _sample_sites = human_sites
    page_type = 'add_sample_human'


class AddAnimalSampleHandler(AddSample):
    _sample_sites = animal_sites
    page_type = 'add_sample_animal'


class AddGeneralSampleHandler(AddSample):
    _sample_sites = general_sites
    page_type = 'add_sample_general'
