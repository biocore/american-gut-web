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

_PARTICIPANT_OVERVIEW = {
    'COMPLETED_CONSENT': 'Completed consent',
    'COMPLETED_SURVEY': 'Completed survey',
    'SAMPLES_ASSIGNED': 'Samples assigned',
    'OVERVIEW_FOR_PARTICPANT': 'Overview for participant'
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

_NEW_PARTICIPANT = {
    'VARIABLE': 'TEXT',
    'ADD_HUMAN_TITLE': 'Add a New Human Source',
    'ADD_HUMAN_HELP_SUGGESTION': 'If you need help with the website, please use the contact mechanism in the menu to the left. Please do not email the people listed in this form for help, unless it has to do with an injury. ',
    'CONSENT_TITLE': 'CONSENT TO PARTICIPATE IN A RESEARCH STUDY',
    'TEXT_TITLE': 'Study Title: American Gut Project',
    'TEXT_PI': 'Principal Investigator: Rob Knight',
    'TEXT_PERSONNEL_TITLE': 'Key Personnel:',
    'TEXT_NAME': 'Name',
    'TEXT_ROLE': 'Role',
    'TEXT_DEPARTMENT': 'Department',
    'TEXT_PHONE': 'Phone Number',
    'TEXT_EMAIL': 'E-mail',
    'TEXT_NAME_1': 'Rob Knight',
    'TEXT_ROLE_1': 'Principal Investigator',
    'TEXT_DEPARTMENT_1': 'Biofrontiers Institute/HHMI',
    'TEXT_PHONE_1': '303-492-1984',
    'TEXT_EMAIL_1': 'Rob.Knight@colorado.edu',
    'TEXT_NAME_2': 'Gail Ackermann',
    'TEXT_ROLE_2': 'Co-I',
    'TEXT_DEPARTMENT_2': 'Biofrontiers Institute',
    'TEXT_PHONE_2': '303-492-7506',
    'TEXT_EMAIL_2': 'Gail.Ackermann@colorado.edu',
    'TEXT_PARTICIPATION_TITLE': 'Your participation in this research study is voluntary.',
    'TEXT_PARTICIPATION_DESCRIPTION': ' Please think about the information below carefully. Feel free to ask questions before making your decision whether or not to participate. If you decide to participate, you will be asked to sign this form electronically and will receive a copy of the form by email at the address you supplied when you signed up for the study.',
    'TEXT_BACKGROUND_TITLE': 'Purpose and Background',
    'TEXT_BACKGROUND_DESCRIPTION_1': 'Trillions of microorganisms live on and within the human body, which is colonized at birth and continuously inhabited throughout a person\'s lifetime. Our resident microbes occupy many body habitats, including the skin and mucosal surfaces, and the gastrointestinal tract. Our microbial symbionts are largely harmless or beneficial; for example, we rely on our gut microbiota to aid in nutrition, resist pathogens, and educate our immune system.  We would like to survey a large number of volunteers from the US and other countries including all body types, all dietary preferences and both healthy and unhealthy people to more clearly define the range of these microbial communities.  We are interested in learning whether people with similar age, diet, environment, family, pets, body weight, or other features, also have similar microorganisms.',
    'TEXT_BACKGROUND_DESCRIPTION_2': 'To accomplish this we will ask you to sample up to 7 sites on your body (skin anywhere on the body, saliva, stool, nostril mucus, vaginal mucus, ear wax or tears) using polyester tipped swabs that will be sent to you at the address you provide with instructions on how to obtain the samples, instructions for safely returning the samples to us and a pre-addressed envelope for returning the samples to us through FedEx or the mail service. You will also be asked to complete the questionnaire online that includes questions about age, diet, environment, family, pets, body weight and current health status.  You will be asked to use a website to determine your average intake of fat, protein, carbohydrates, vegetables and grains for 7 days prior to sampling.  The samples will have a code label attached to them so that we can identify who sent them to us but no personally identifying information. Some people may be asked to keep a food diary detailing everything they eat and drink every day for up to 6 months.  We may also request additional samples from certain participants that are of particular interest because of their health status and/or dietary preferences (a maximum of 7 times).  We anticipate that the entire study will be completed in 5 years. When the results are available for your samples we will provide you with an easy to understand summary of the microbial communities of your body and a summary of the combined results of other participants for comparison.  We anticipate that the results for your samples will be available within 3-6 months of receipt in the laboratory. These results will be sent to you by email. ',
    'TEXT_BACKGROUND_DESCRIPTION_3': 'We are requesting that you contribute funding to the project at a level that is commensurate with the number of swabs and the kinds of tests you are requesting.  The basic package covers a single fecal swab.',
    'TEXT_STUDY_TASK_TITLE': 'Study Tasks and Procedures',
    'TEXT_STUDY_TASK_DESCRIPTION': 'If you agree to participate in this study you will be asked for your name ,  and to donate samples, to complete a questionnaire and to provide updated personal information. We will send you a sample kit that includes the swabs (which are individually wrapped in plastic and include a plastic sleeve for returning the sample to us), coded labels for the sample tubes, and a pre-addressed envelope with instructions on how to safely  return the samples to us for analysis.  ',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_TITLE': 'Samples may include',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_1': 'Stool (fecal) by collecting a smear from used bathroom tissue using a sterile polyester-tip swab',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_2': 'Saliva using a sterile polyester-tip swab inserted into the mouth and sampling the surface of the tongue or inside of your cheek',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_3': 'Skin using a sterile polyester-tip swab',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_4': 'Nostril mucus by inserting a sterile polyester-tip swab gently into a nostril',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_5': 'Vaginal mucus by inserting a sterile polyester-tip swab into the introitus of the vagina',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_6': 'Ear wax by inserting a sterile polyester-tip swab gently into the ear',
    'TEXT_STUDY_TASK_DESCRIPTION_LIST_7': 'Tears by inserting a sterile polyester-tip swab gently along the inner corner of the eyelid (avoiding contact with the eye).',
    'TEXT_STUDY_TASK_DESCRIPTION_ADDITIONAL_1': 'Examples of areas of skin that may be swabbed include the forehead, and left and right palms.',
    'TEXT_STUDY_TASK_DESCRIPTION_ADDITIONAL_2': 'After you submit your first set of samples, we may ask you to donate additional samples (up to 7 times) if you belong to a group that has specific diet, disease or age considerations.  You will be contacted by email if we would like to repeat the sampling. Some participants will be asked to provide a detailed food diary that includes a list of everything you eat and drink every day for up to 6 months. If this is required we will contact you by email to confirm that you are willing to contribute this information.',
    'TEXT_INTERNATIONAL_PARTICIPANT_TITLE': 'International Participants',
    'TEXT_INTERNATIONAL_PARTICIPANT_DESCRIPTION': 'In order to comply with amended federal regulations and IATA regulations we are requesting that international participants return their sample tubes through FedEx international and follow additional requirements for safely shipping human swab samples.  You will need to use the airway bill we send to you  for shipment that clearly identifies the samples as "human exempt specimens".  The samples will be packaged with secondary containment to ensure that they can be safely returned.  For this you will use tape to seal the plastic tube that contains the swab, place the swab in a buff mailing envelope and place the buff envelope inside the Tyvek/plastic mailer prior to FedEx shipment.  If you do not follow these directions the sample will be intercepted at the port of entry into the USA and destroyed.',
    'TEXT_SURVEY_DESCRIPTION_TITLE': 'Description of Surveys/Questionnaires/Interview Questions',
    'TEXT_SURVEY_DESCRIPTION_DESCRIPTION_1': 'You will be asked questions about your general personal information (age, sex, height, weight, ethnicity, place of birth, current ZIP code. We will ask if you recently moved and where you moved from., We will ask questions about general diet information (including whether you follow a special diet, if you have food allergies, whether you have cultural or religious food restrictions). Other questions address whether you have pets and the type of contact you have with these pets and your relationship to other people in this study.  There is a section on health information including a history of allergies/asthma, if you suffer from migraines and if you have a history of irritable bowel disease.  The questionnaire also asks you to complete a food log to assess the amount of protein, fat, carbohydrate, grains and vegetables in your diet. For this we suggest that you contact a free website that will allow you to estimate these amounts.',
    'TEXT_SURVEY_DESCRIPTION_DESCRIPTION_2': 'Some participants may be asked to keep a detailed food diary for up to 6 months listing all the foods they eat and drink in a day.',
    'TEXT_DURATION_TITLE': 'Duration',
    'TEXT_DURATION_DESCRIPTION': 'We anticipate that participant time commitment for sampling will be less than 15 minutes; to complete the questionnaire online will take no more than 45 minutes; and completing the food diary should take no more than10 minutes/day.  The study will be conducted over a maximum period of 5 years to include all the people we are requesting permission to sample.  We anticipate that results will be available within 3-6 months of sample receipt.',
    'TEXT_WITHDRAWAL_TITLE': 'Study Withdrawal',
    'TEXT_WITHDRAWAL_DESCRIPTION_1': 'Taking part in this study is completely voluntary.  You do not have to participate if you do not want to.  You may also leave the study at any time.  If you leave the study before it is finished, there will be no penalty to you, and you will not lose any benefits to which you are otherwise entitled.',
    'TEXT_WITHDRAWAL_DESCRIPTION_2': 'To withdraw from the study send email to the American Gut Project (www.humanfoodproject.com/american-gut/) using the email address you used to contact us about the study and include your access code so that we can delete your records.',
    'TEXT_RISKS_TITLE': 'Risks and Discomforts',
    'TEXT_RISKS_DESCRIPTION_1': 'There are no foreseeable risks for participating in this study.  You should be aware that the samples you submit are not anonymous but we will make every effort to ensure that they remain confidential.  The only staff associated with the study that will have access to confidential information (your name and address) will be those responsible for shipping the sample kit and questionnaire to you.  When the samples are returned they will have an associated code but no personally identifiable information.',
    'TEXT_BENEFITS_TITLE': 'Benefits',
    'TEXT_BENEFITS_DESCRIPTION': 'You may not receive any direct benefit from taking part in this study other than you or your child\'s intrinsic interest in the scientific outcome.',
    'TEXT_CONFIDENTIALITY_TITLE': 'Confidentiality',
    'TEXT_CONFIDENTIALITY_DESCRIPTION_1': 'We will make every effort to maintain the privacy of your or your child\'s data. All data will transferred electronically to a secure database stored on a server (The beast) in a CU card access-controlled server room. There is no public accessibility to this server without VPN and a password. The code key will be stored in a single location on a password-protected database on a server in a CU-access card controlled server room. The code will be destroyed by deletion from the server at the end of the study.  All other data including all electronic data will be de-identified (coded).',
    'TEXT_CONFIDENTIALITY_LIST_TITLE': 'These are some reasons that we may need to share the information you give us with others:',
    'TEXT_CONFIDENTIALITY_LIST_1': 'If it is required by law.',
    'TEXT_CONFIDENTIALITY_LIST_2': 'If we think you or someone else could be harmed.',
    'TEXT_CONFIDENTIALITY_LIST_3': 'Sponsors, government agencies or research staff sometimes look at forms like this and other study records. They do this to make sure the research is done safely and legally. Organizations that may look at study records include:',
    'TEXT_CONFIDENTIALITY_LIST_4': 'Office for Human Research Protections or other federal, state, or international regulatory agencies',
    'TEXT_CONFIDENTIALITY_LIST_5': 'The University of Colorado Boulder Institutional Review Board',
    'TEXT_CONFIDENTIALITY_LIST_6': 'The sponsor or agency supporting the study: Howard Hughes Medical Institute and the American Gut Project.',
    'TEXT_COMPENSATION_TITLE': 'Compensation',
    'TEXT_COMPENSATION_DESCRIPTION': 'You will not receive any compensation for participating in this research.',
    'TEXT_RIGHTS_TITLE': 'Participant Rights',
    'TEXT_RIGHTS_DESCRIPTION': 'Taking part in this study is your choice. You may choose either to take part or not take part in the study. If you decide to take part in this study, you may leave the study at any time. No matter what decision you make, there will be no penalty to you in any way. You will not lose any of your regular benefits. We will tell you if we learn any new information that could change your mind about being in this research study. For example, we will tell you about information that could affect your health or well-being.',
    'TEXT_INJURIES_TITLE': 'If You are Injured',
    'TEXT_INJURIES_DESCRIPTION': 'Please call Rob Knight at 303-492-1984 or email <a href="mailto:Rob.Knight@colorado.edu">Rob Knight</a>.',
    'TEXT_QUESTIONS_TITLE': 'Contacts and Questions',
    'TEXT_QUESTIONS_DESCRIPTION_1': 'For questions, concerns, or complaints about this study, call please call Rob Knight at 303-492-1984 or email <a href="mailto:Rob.Knight@colorado.edu">Rob Knight</a>.',
    'TEXT_QUESTIONS_DESCRIPTION_2': 'If you are injured as a result of participating in this study or for questions about a study-related injury, call Please call Rob Knight at 303-492-1984 or email <a href="mailto:Rob.Knight@colorado.edu">Rob Knight</a>.',
    'TEXT_QUESTIONS_DESCRIPTION_3': 'If you have questions about your rights as a research study participant, you can call the Institutional Review Board (IRB). The IRB is independent from the research team. You can contact the IRB if you have concerns or complaints that you do not want to talk to the study team about. The IRB phone number is (303) 735-3702.',
    'TEXT_I_HAVE_READ': ' I have read (or someone has read to me) this form. I am aware that I am being asked to provide personally identifying information so that I can be considered for inclusion into the study. I voluntarily agree to provide this information. I am not giving up any legal rights by signing this form. I will be sent a copy of this form by e-mail.',
    'PARTICIPANT_NAME': 'Name of participant',
    'PARTICIPANT_EMAIL': 'Email of participant',
    'PARTICIPANT_AGE_CONFIRMATION': 'Participant is 13 years of age or younger',
    'PARTICIPANT_IS_YOUNG': 'Participant is older than 3 months and younger than 7 years of age',
    'PARTICIPANT_IS_YOUNG_2': 'Participant is between 7 and 13 years of age',
    'PARTICIPANT_PARENT_1': 'Name of parent/guardian 1',
    'PARTICIPANT_PARENT_2': 'Name of parent/guardian 2',
    'PARTICIPANT_DECEASED_PARENTS': 'One or both parents are deceased or unable to consent.'
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

# Actual text locale
text_locale = {
    'FAQ.html': _FAQ,
    'db_error.html': _DB_ERROR,
    'retrieve_kitid.html': _RETREIVE_KITID,
    'error.html': _ERROR,
    'forgot_password.html': _FORGOT_PASSWORD,
    'help_request.html': _HELP_REQUEST,
    'new_participant.html': _NEW_PARTICIPANT,
    'participant_overview.html': _PARTICIPANT_OVERVIEW,
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
