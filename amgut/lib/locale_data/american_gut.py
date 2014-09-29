#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


# Template specific dicts
_FAQ = {'FAQ_0_WHAT_IS_A_GUT': 'asdasdasd'}
_TAXA_SUMMARY = {'RESOLUTION_NOTE': "Note: Where there are blanks in the table below, the taxonomy could not be resolved in finer detail.",
                 'PERCENTAGES_NOTE': "Note: The percentages listed represent the relative abundance of each taxon. This summary is based off of normalized data. Because of limitations in the way the samples are processed, we cannot reliably obtain species level resolution. As such, the data shown are collapsed at the genus level.",
                 'DOWNLOAD_LINK': "Download the table"}
_HELP_REQUEST = {
    'CONTACT_HEADER': "Contact the American Gut",
    'RESPONSE_TIMING': "We will send a response to the email address you supply within 24 hours.",
    'FIRST_NAME': "First name",
    'LAST_NAME': "Last name",
    'EMAIL_ADDRESS': "Email address",
    'PROBLEM_PROMPT': "Enter information related to your problem"
}

_DB_ERROR = {
    'HEADER': 'Oops! There seems to be a database error.',
    'MESSAGE': 'Please help us to debug by emailing us at <a href="mailto:%(help_email)s">%(help_email)s</a> and tell us exactly what happend before you got this error.',
    'SIGNOFF': 'Thanks, <br /> The American Gut Team'
}

_SAMPLE_OVERVIEW = {
    'BARCODE_RECEIVED': 'Sample %(barcode)s. This sample has been received by the sequencing center!',
    'DISPLAY_BARCODE': 'Sample %(barcode)s',
    'RESULTS_PDF_LINK': 'Click this link to visualize sample %(barcode)s in the context of other microbiomes!',
    'SAMPLE_NOT_PROCESSED': 'This sample has not yet been processed. Please check back later.',
    'DATA_VIS_TITLE': 'Data Visualization',
    'TAXA_SUM_TITLE': 'Taxa Summary',
    'VIEW_TAXA_SUMMARY': 'View Taxa Summary',
    'SAMPLE_STATUS': 'Sample Status',
    'SAMPLE_SITE': 'Sample Site',
    'SAMPLE_DATE': 'Sample Date',
    'SAMPLE_TIME': 'Sample Time',
    'SAMPLE_NOTES': 'Notes',
    'REMOVE_BARCODE': 'Remove barcode %(barcode)s'
}
_CONSTRUCTION = {
    'WELCOME': 'Welcome - you have reached the participant login page for the American Gut Project. Thanks again for joining the study - we appreciate your support. This is our first citizen science project so we are still working out some kinks. A few things:',
    'MAIN_TEXT': '<li>We are making final changes and additions to the online consent form you will sign and the questionnaire you will be asked to fill out. The American Gut developers team is working double-time to get this done, as are a lot of other people in our lab at University of Colorado. So please come back to this page in a few days.</li><li>When the site is live, you will be able to log in and sign the consent form. Please, do not take your sample and mail back to us before you sign the online consent form. If you have any questions e-mail <a href="mailto:%(help_email)s">us</a>.</li><li>Since we will be asking you for a week\'s worth of dietary info in the questionnaire, it would be great if you could get a head start on that now. Note we ask that you take your sample AFTER you have recorded your dietary info for a week. There are a number of FREE online dietary tools out there - we recommend Calorie Count. Note we will be asking questions about your carb, protein, fat, alcohol, and fiber intake, (as a percentage of your total intake) as well as some info on types of food. So, use a tool that allows you to enter as much detail as possible.</li>',
    'FOOTER': 'Again, we appreciate your patience. Everyone is working hard on our end to make this project as interesting as possible for everyone. If you have any questions, please email us at %(help_email)s.'
}

_FORGOT_PASSWORD = {'ENTER_ID_EMAIL': 'Enter your Kit ID and email',
                    'KIT_ID': 'Kit ID:',
                    'EMAIL': 'E-mail',
                    'EMAIL_RESET_PASSWORD': 'You will receive an email shortly with instructions to reset your password. Please check your email because you need to reset your password within two hours.',
                    'EMAIL_FAILED': '<p>There was a problem sending you the password reset code. Please contact us directly at <a href=\"mailto:%(help_email)s\" target=\"_blank\">%(help_email)s</a>.</p><p>Email contained: </p><p>{{message}}</p>',
                    'NO_RECORD': '<p style="color:red;">This information does not match our records</p><p>Please email <a href="mailto:%(help_email)s">directly</a> for further assistance<p>',
                    'SEND_EMAIL': 'Send email'}

_ERROR = {
    'ERROR_OCCURED': 'AN ERROR HAS OCCURED!',
    'ERROR_CONTACT': 'Please copy the following into an email and send this information, along with the url you were trying to access, to <a href="mailto:info@americangut.org">info@americangut.org</a>'
    }

_RETREIVE_KITID = {
    'UNKNOWN_EMAIL': 'This email address is not in our system',
    'ENTER_EMAIL': 'Please Enter Your Email',
    'SEND_EMAIL': 'Send Kit ID Email',
    'EMAIL_SUCCESS': 'Your kit ID has been emailed to you. Please check your email.',
    'EMAIL_CANTSEND': 'Mail can be sent only from microbio.me domain.',
    'EMAIL_EXCEPTION': 'There was a problem sending you the kit ID. Please contact us directly at <a href=\"mailto:info@americangut.org\">info@americangut.org</a>.',
    'EMAIL_PROMPT': 'Email:'
    }

_REGISTER_USER = {
    'ENTER_NAME': 'Please enter your name',
    'ENTER_EMAIL': 'Please enter your email',
    'REQUIRED_EMAIL': 'You must supply a valid email',
    'ENTER_ADDRESS': 'Please enter your address',
    'ENTER_CITY': 'Please enter your city',
    'ENTER_STATE': 'Please enter your state',
    'ENTER_ZIP': 'Please enter your zip',
    'ENTER_COUNTRY': 'Please enter your country',
    'REQUIRED_ZIP': 'Your zip must consist of at least 5 characters',
    'EMAIL': 'Email',
    'NAME': 'Name',
    'ADDRESS': 'Address',
    'CITY': 'City',
    'STATE': 'State',
    'ZIP': 'Zip',
    'COUNTRY': 'Country',
    'SUBMIT': 'Submit My Information'
}

_PORTAL = {
'GREETING': 'Hi %(user_name)s! Please follow the steps below.',
'VERIFY_TAB': 'Verify Your Kit',
'ADD_SOURCE_TAB': 'Add Source <br>Survey',
'TAKE_SAMPLE_TAB': 'Take a Sample',
'LOG_SAMPLE_TAB': 'Log a Sample',
'MAIL_TAB': 'Mail Samples <br>to Us',
'SEQ_TAB': 'Sequencing &amp;<br>Results',
'VERIFICATION_HEADER_1': 'Verification',
'VERIFICATION_TEXT_1': 'We ask you to verify that you received the correct sample tubes and kit. Using a <strong>Verification Code</strong> helps us ensure that you receive the correct barcodes and Credentials Sheet.',
'VERIFICATION_TEXT_2': 'our <strong>Verification Code</strong> will be sent to you via email to the address that you entered when you made your donation; if you made an anonymous donation, please <a href="/authed/help_request/">contact us directly</a>.',
'VERIFICATION_TEXT_3': 'If you cannot find your <strong>Verification Code</strong>, please make sure to check your spam folder. If you still cannot find the code, please <a href="/authed/help_request/">contact us</a>.',
'VERIFICATION_HEADER_2': 'Verify your identity and kit barcode(s)',
'VERIFICATION_CODE_PROMPT': 'Please enter the verification code sent to your email address <a href="#" class="help" title="If you did not recieve a verification code in your email from American Gut, please check your spam folder. If you still can not find it, contact %(help_email)s">(?)</a>',
'VERIFICATION_CODE_ERROR': 'The kit verification code you entered does not match our records. Please double-check the code you entered. If you continue to experience difficulties, please <a href=/authed/help_request/>contact us</a>.',
'VERIFY_BARCODES': 'Please verify that the barcode(s) you received in the mail match the barcode(s) here',
'VERIFY_BARCODES_POPUP': 'The barcode you need to verify is located on the outside of your sample tube.',
'SAMPLE_SOURCE_HEADER_1': 'Sample Source',
'SAMPLE_SOURCE_TEXT_1': 'There are three different sample sources that you can choose from for the %(project)s. The sources are human, animal and environmental. The buttons below will allow you to add a new sample source.',
'SAMPLE_SOURCE_TEXT_2': 'If you add a <strong>human</strong> source, you will need to have a completed 7 day food diary for that human. If you add a <strong>human</strong> or <strong>animal</strong> source, you will be asked to complete a survey',
'SAMPLE_SOURCE_TYPE_HUMAN': 'Human',
'SAMPLE_SOURCE_TYPE_ANIMAL': 'Animal',
'SAMPLE_SOURCE_TYPE_ENVIRONMENTAL': 'Environmental',
'SURVEY_HEADER_1': 'Survey',
'SURVEY_TEXT_1': 'If you are taking a human or animal sample, we ask that you complete a survey.',
'SURVEY_TEXT_2': 'The survey will take <strong>30-45 minutes</strong> for a human subject, or <strong>10 minutes</strong> for an animal subject. You <strong>cannot</strong> save in the middle of the survey, so please set aside enough time to complete the entire survey.',
'SURVEY_TEXT_3': 'If you are taking a human sample, the survey includes demographic, lifestyle, medical and diet questions. All survey questions are optional.',
'SURVEY_TEXT_4': 'The 7 day food diary is used when answering the human survey, so please be sure to have that ready <strong>before</strong> starting the survey. We strongly recommend using <a href="http://caloriecount.about.com/">CalorieCount</a> to record dietary intake, though you are free to use whatever method you find most convenient. A screenshot of the dietary questions is shown below, <strong>please make sure to use a tool that will allow you to accurately answer these questions</strong>.',
'SURVEY_TEXT_5': 'Additionally, <a href="http://titojankowski.com">Tito Jankowski</a> has compiled a <a href="http://titojankowski.com/american-gut-how-to/">comprehensive guide</a> on how to do this if you are a <a href="http://www.myfitnesspal.com">MyFitnessPal</a> user.',
'SAMPLE_STEPS_HEADER_1': 'Before Taking Your Samples',
'SAMPLE_STEPS_TEXT_1': 'These are the steps involved in taking a sample:',
'SAMPLE_STEPS_TEXT_2': '<li>Make sure you have <a href="#" onclick="selectTab(\'source\')">added your sample source and complete the required survey(s)</a></li><li>Remove the sample swabs from the sample tube</li><li>Collect your sample following the guidelines below</li><li>Place sample swabs into the sample tube</li>',
'SAMPLE_STEPS_TEXT_3': 'These sample collection instructions are very important, please read through them <strong>before</strong> beginning to take your sample. Deviations will cause issues with sample processing, sequencing, and data analysis. We cannot guarantee that we will be able to process your sample if the instructions are not followed, and <strong>we cannot offer replacements if instructions were not followed</strong>. Please do not hesitate to ask us questions at <a href="/authed/help_request/">%(help_email)s</a>.',
'SAMPLE_STEPS_HEADER_2': 'Taking Your Samples',
'SAMPLE_STEPS_TEXT_4': 'Once you have removed the sample tube, only handle the sample swab by the red cap.',
'SAMPLE_STEPS_TEXT_5': 'For a <strong>fecal sample</strong>, rub both cotton tips on a fecal specimen (a used piece ofbathroom tissue). Collect a small amount of biomass. Maximum collection would be to saturate 1/2 a swab. <strong>More is not better!</strong> The ideal amount of biomass collected is shown below.',
'SAMPLE_STEPS_TEXT_6': 'For an <strong>oral sample</strong>, firmly rub both sides of both cotton tips on the surface of the tongue for 20 seconds. Take great caution not to touch the cheeks, teeth, or lips.',
'SAMPLE_STEPS_TEXT_7': 'For a <strong>skin sample</strong>, firmly rub both sides of both cotton tips over the skin surface being sampled for 20 seconds.',
'SAMPLE_STEPS_TEXT_8': 'For an <strong>other/environmental sample</strong>, firmly rub both sides of both cotton tips over the surface being sampled for 20 seconds.',
'SAMPLE_STEPS_TEXT_9': 'After you have finished taking your sample, return the swabs to the sample tube and push the red cap on firmly.',
'LOG_SAMPLE_HEADER_1': 'Logging Samples',
'LOG_SAMPLE_TEXT_1': 'Please write the sample site, date, and time on the sampling tube.',
'LOG_SAMPLE_TEXT_2': 'After writing the information on the sampling tube tube, <a href="/authed/add_sample_overview/">log the sample</a> in our system.',
'MAILING_HEADER_1': 'Mailing samples',
'MAILING_TEXT_1': 'Once you have added a <a href="#" onclick="selectTab(\'source\')">sample source, completed the relevant survey</a> (if applicable), <a href="#" onclick="selectTab(\'sample\')">taken</a> and <a href="#" onclick="selectTab(\'log\')">logged your samples</a>, you should then mail the samples back to us.',
'MAILING_TEXT_2': 'Wrap the sample tube in absorbent tissue, such as facial tissue or paper towels, and mail it back as soon as possible. The absorbent tissue will help to keep the relative humidity within the package low.',
'MAILING_TEXT_3': 'We also recommend using a reinforced envelope to reduce the chance of losing your sample due to damaged packaging.',
'MAILING_TEXT_4': 'The sooner we receive your sample, the sooner we can get it stored in our -80C freezers and ready for processing!',
'MAILING_TEXT_5': '<strong>Do not refrigerate or freeze the samples</strong> if they cannot be shipped immediately. Store them in a cool dry place such as a cabinet or a closet.',
'DOMESTIC_HEADER_1': 'Domestic Shipping',
'DOMESTIC_TEXT_1': 'Shipping within the US should be less than $1.50, but we recommend taking the sample to the post office to get the proper postage. Getting the postage right on the first try is important since samples that spend a long time in transit will likely not produce the highest quality results.',
'DOMESTIC_TEXT_2': 'This is the shipping address:',
'DOMESTIC_TEXT_3': 'American Gut Project<br />Knight Lab, JSCBB<br />596 UCB<br />Boulder, CO 80309',
'INTERNATIONAL_HEADER_1': 'International Shipping',
'INTERNATIONAL_TEXT_1': 'In order to comply with amended federal and IATA regulations, we are requesting that international participants return their sample tubes through FedEx International and that international participants follow the additional safely requirements for shipping human swab samples to the United States. Your airway bill must clearly identify the package as containing "human exempt specimens". The samples will additionally need to be packaged within a secondary containment to ensure that they can safely enter the United States.',
'INTERNATIONAL_TEXT_2': 'For shipment, you will need to use clear tape to secure the sample swabs to the sample tube, then place the sample tube in the provided buff mailing envelope. Then place the buff envelope inside a Tyvek/plastic mailer, <strong>which can be acquired free of charge from FedEx</strong>, when shipping the sample, prior to FedEx shipment.',
'INTERNATIONAL_TEXT_3': 'If you do not follow these directions the sample will be destroyed by United States Customs at the port of entry into the United States.',
'INTERNATIONAL_HEADER_2': 'Your samples',
'INTERNATIONAL_TEXT_4': '<li>Are considered dried specimens</li><li>Must be shipped via FedEx</li><li>Must have tape to sealing the plastic tube that contains the swab</li><li>Must be placed in a buff mailing envelope with the buff envelope placed inside a Tyvek/plastic mailer prior to FedEx shipment</li><li>Must be shipped with an airway bill and must be labeled with the complete address of the sender and complete address of recipient, and with the words "Human exempt sample(s)"</li>',
'RESULTS_HEADER_1': 'Sequencing &amp; Results',
'RESULTS_TEXT_1': 'Once you have added a <a href="#" onclick="selectTab(\'source\')">sample source, completed the relevant survey</a> (if applicable), <a href="#" onclick="selectTab(\'sample\')">taken</a> and <a href="#" onclick="selectTab(\'log\')">logged your samples</a> and you have <a href="#" onclick="selectTab(\'mail\')">mailed the samples back to us</a>, we will then perform sequencing and analysis on your samples.',
'RESULTS_TEXT_2': 'Sequencing and data analysis can take up to 6 months, please be patient! We will let you know as soon as your samples have been sequenced and analyzed.',
'RESULTS_READY_HEADER_1': 'Your results are ready!',
'RESULTS_READY_TEXT_1': 'One or more of the samples you submitted have been sequenced, and the results are now available online! We will be mailing hardcopies of these results shortly. Currently, we have only processed fecal samples, but we will be processing samples from other body sites soon.',
'RESULTS_READY_TEXT_2': 'To access your available results, hover over "Human Samples" in the menu on the left, hover over your name, then click on your sample to view your results, or click one of the links below. The following barcodes are ready:',
'RESULTS_READY_TEXT_3': 'You will be able to view your results here on this website once they are available.'
}

# Actual text locale
text_locale = {
    'FAQ.html': _FAQ,
    'portal.html': _PORTAL,
    'db_error.html': _DB_ERROR,
    'retrieve_kitid.html': _RETREIVE_KITID,
    'error.html': _ERROR,
    'forgot_password.html': _FORGOT_PASSWORD,
    'help_request.html': _HELP_REQUEST,
    'sample_overview.html': _SAMPLE_OVERVIEW,
    'taxa_summary.html': _TAXA_SUMMARY,
    'construction.html': _CONSTRUCTION,
    'register_user.html': _REGISTER_USER
    }

# Any media specific localizations
media_locale = {'LOGO': '/static/img/ag_logo.jpg',
                'HELP_EMAIL': 'info@americangut.org',
                'PROJECT_TITLE': 'American Gut Project',
                'FAVICON': '/static/img/favicon.ico',
                'FUNDRAZR_URL': 'https://fundrazr.com/campaigns/4Tqx5',
                'NAV_PARTICIPANT_RESOURCES': 'Participant resources',
                'NAV_HOME': 'Home',
                'NAV_MICROBIOME_101': 'American Gut 101',
                'NAV_FAQ': 'FAQ',
                'NAV_MICROBIOME_FAQ': 'Human Microbiome FAQ',
                'NAV_ADDENDUM': 'How do I interpret my results?',
                'NAV_PRELIM_RESULTS': 'Preliminary results!',
                'NAV_CHANGE_PASSWORD': 'Change Password',
                'NAV_CONTACT_US': 'Contact Us',
                'NAV_LOGOUT': 'Log out',
                'NAV_HUMAN_SAMPLES': 'Human Samples',
                'NAV_RECEIVED': '(Received)',
                'NAV_ADD_HUMAN': 'Add Human Source',
                'NAV_ANIMAL_SAMPLES': 'Animal Samples',
                'NAV_ADD_ANIMAL': 'Add Animal Source',
                'NAV_ENV_SAMPLES': 'Environmental Samples',
                'NAV_LOG_SAMPLE': 'Log Sample',
                'NAV_JOIN_PROJECT': 'Join The Project',
                'NAV_KIT_INSTRUCTIONS': 'Kit Instructions',
                'NAV_PARTICIPANT_LOGIN': 'Participant Log In',
                'NAV_FORGOT_KITID': 'I forgot my kit ID',
                'NAV_FORGOT_PASSWORD': 'I forgot my password'
                }
