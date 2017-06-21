#!/usr/bin/env python
from __future__ import division
from amgut.lib.config_manager import AMGUT_CONFIG

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

# Any media specific localizations
HELP_EMAIL = "info@americangut.org"

_SITEBASE = AMGUT_CONFIG.sitebase

media_locale = {
    'LOCALE': AMGUT_CONFIG.locale,
    'SITEBASE': _SITEBASE,
    'LOGO': _SITEBASE + '/static/img/ag_logo.jpg',
    'ANALYTICS_ID': 'UA-55353353-1',
    'LATITUDE': 39.83,
    'LONGITUDE': -99.89,
    'ZOOM': 4,
    'STEPS_VIDEO': "http://player.vimeo.com/video/63542787",
    'ADD_PARTICIPANT': 'http://player.vimeo.com/video/63931218',
    'ADD_PARTICIPANT_IMG_1': _SITEBASE + "/static/img/add_participant.png",
    'ADD_PARTICIPANT_IMG_MENU': _SITEBASE + "/static/img/add_participant_menu.png",
    'LOG_SAMPLE_OPTS': _SITEBASE + "/static/img/log_sample_options.png",
    'ADD_SAMPLE_HIGHLIGHT': _SITEBASE + "/static/img/add_sample_highlight.png",
    'ADD_SAMPLE_OVERVIEW': _SITEBASE + "/static/img/add_sample_overview.png",
    'FAQ_AMBIGUOUS_PASS': _SITEBASE + '/static/img/creds_example.png',
    'SAMPLE_BARCODE': _SITEBASE + '/static/img/sample_barcode.jpg',
    'SWAB_HANDLING': 'http://player.vimeo.com/video/62393487',
    'HELP_EMAIL': HELP_EMAIL,
    'PROJECT_TITLE': AMGUT_CONFIG.project_name,
    'FAVICON': _SITEBASE + '/static/img/favicon.ico',
    'FUNDRAZR_URL': 'https://fundrazr.com/campaigns/4Tqx5',
    'NAV_PARTICIPANT_RESOURCES': 'Participant resources',
    'NAV_HOME': 'Home',
    'NAV_MICROBIOME_101': '%s 101' % AMGUT_CONFIG.project_shorthand,
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
    'NAV_LOG_SAMPLE': 'Assign Sample',
    'NAV_JOIN_PROJECT': 'Join The Project',
    'NAV_KIT_INSTRUCTIONS': 'Kit Instructions',
    'NAV_PARTICIPANT_LOGIN': 'Participant Log In',
    'NAV_REGISTER_KIT': 'Register Kit',
    'NAV_FORGOT_KITID': 'I forgot my kit ID',
    'NAV_INTERNATIONAL': 'International Shipping',
    'NAV_FORGOT_PASSWORD': 'I forgot my password',
    'ADDENDUM_CERT_TITLE': _SITEBASE + '/static/img/Michael_Pollan_mod-01.png',
    'ADDENDUM_CERT_NAME': _SITEBASE + '/static/img/Michael_Pollan_mod-01b.png',
    'ADDENDUM_CERT_HEADER': _SITEBASE + '/static/img/Michael_Pollan_mod-02.png',
    'ADDENDUM_CERT_BARCHART': _SITEBASE + '/static/img/Michael_Pollan_mod-11.png',
    'ADDENDUM_CERT_BARCHART_LEGEND': _SITEBASE + '/static/img/Michael_Pollan_mod-12.png',
    'ADDENDUM_CERT_ABUNDANT_MICROBES': _SITEBASE + '/static/img/Michael_Pollan_mod-13.png',
    'ADDENDUM_CERT_ENRICHED_MICROBES': _SITEBASE + '/static/img/Michael_Pollan_mod-14.png',
    'ADDENDUM_CERT_RARE_MICROBES': _SITEBASE + '/static/img/Michael_Pollan_mod-15.png',
    'ADDENDUM_CERT_HEADER_PCOA': _SITEBASE + '/static/img/Michael_Pollan_mod-03.png',
    'ADDENDUM_CERT_PCOA_LEGEND': _SITEBASE + '/static/img/Michael_Pollan_mod-04.png',
    'ADDENDUM_CERT_PCOA_BODYSITES': _SITEBASE + '/static/img/Michael_Pollan_mod-08.png',
    'ADDENDUM_CERT_PCOA_AGES_POP': _SITEBASE + '/static/img/Michael_Pollan_mod-09.png',
    'ADDENDUM_CERT_PCOA_AG_POPULATION': _SITEBASE + '/static/img/Michael_Pollan_mod-10.png',
    'ADDENDUM_TAX_BARCHART': _SITEBASE + '/static/img/TaxFig.png',
    'ADDENDUM_PCOA_BODYSITES': _SITEBASE + '/static/img/PCoA1.png',
    'ADDENDUM_PCOA_AGES_POPS': _SITEBASE + '/static/img/PCoA2.png',
    'ADDENDUM_PCOA_AG_POPULATION': _SITEBASE + '/static/img/PCoA3.png',
    'PORTAL_DIET_QUESTIONS': _SITEBASE + '/static/img/diet_questions.png',
    'PORTAL_SHIPPING': _SITEBASE + '/static/img/shipping.png',
    'EMAIL_ERROR': "There was a problem sending your email. Please contact us directly at <a href='mailto:%(help_email)s'>%(help_email)s</a>" % {'help_email': HELP_EMAIL},
    'EMAIL_SENT': 'Your message has been sent. We will reply shortly',
    'SHIPPING_ADDRESS': "University of California, San Diego<br>Knight Lab/ATTN: Greg Humphrey<br>BRF II Room 1220D<br>9500 Gilman Drive, MC 0763<br>La Jolla, CA 92093-0763",
}

_HANDLERS = {
    'PARTICIPANT_EXISTS': 'Participant %s already exists!',
    'MISSING_NAME_EMAIL': 'Missing participant name or email. Please retry, adding all required information.',
    'SUCCESSFULLY_ADDED': "Successfully added %s!",
    'SUCCESSFULLY_EDITED': "Successfully edited %s!",
    'AUTH_REGISTER_SUBJECT': "%(project_shorthand)s Verification Code" % {'project_shorthand': AMGUT_CONFIG.project_shorthand},
    'AUTH_REGISTER_PGP': "\n\nFor the PGP cohort, we are requesting that you collect one sample from each of the following sites:\n\nLeft hand\nRight hand\nForehead\nMouth\nFecal\n\nThis is important to ensure that we have the same types of samples for all PGP participants which, in turn, could be helpful in downstream analysis when looking for relationships between the microbiome and the human genome\n\n.",
    'AUTH_REGISTER_BODY': "Thank you for registering with the %(project_name)s! Your verification code is:\n\n{0}\n\nYou will need this code to verifiy your kit on the %(project_shorthand)s webstite. To get started, please log into:\n\nhttp://microbio.me/AmericanGut\n\nEnter the kit_id and password found inside your kit, verify the contents of your kit, and enter the verification code found in this email.{1}\n\nSincerely,\nThe %(project_shorthand)s Team" % {'project_shorthand': AMGUT_CONFIG.project_shorthand, 'project_name': AMGUT_CONFIG.project_name},
    'KIT_REG_SUCCESS': 'Kit registered successfully.',
    'INVALID_KITID': "Invalid Kit ID or Password",
    'ADD_KIT_ERROR': "Could not add kit to database.  Did you hit the back button while registering and press 'register user' again?",
    'ADD_BARCODE_ERROR': "Could not add barcode to database. Did you hit the back button while registering and press 'register user' again?",
    'CHANGE_PASS_BODY': 'This is a courtesy email to confirm that you have changed your password for your kit with ID %s. If you did not request this change, please email us immediately at {0}'.format(media_locale['HELP_EMAIL']),
    'CHANGE_PASS_SUBJECT': '%(project_shorthand)s Password Reset' % {'project_shorthand': AMGUT_CONFIG.project_shorthand},
    'RESET_PASS_BODY': 'The password on American Gut Kit ID %s  has been reset please click the link below within two hours\nhttp://microbio.me/americangut/change_pass_verify/?email=%s&kitid=%s&passcode=%s',
    'MINOR_PARENTAL_BODY': "Thank you for your interest in this study. Because of your status as a minor, we will contact you within 24 hours to verify parent/guardian consent.",
    'MESSAGE_SENT': "Your message has been sent. We will reply shortly",
    'KIT_IDS_BODY': 'Your {1} Kit IDs are %s. You are receiving this email because you requested your Kit ID from the {1} web page If you did not request your Kit ID please email {0} Thank you,\n The {1} Team\n'.format(media_locale['HELP_EMAIL'], AMGUT_CONFIG.project_shorthand),
    'KIT_IDS_SUBJECT': '%(project_shorthand)s Kit ID' % {'project_shorthand': AMGUT_CONFIG.project_shorthand},
    'BARCODE_ERROR': "ERROR: No barcode was requested",
    'AUTH_SUBJECT': "You have registered your kit!  Your verification code is below.",
    'REGISTER_KIT': 'Kit has not been registered. Please click "Register Kit" link.'
}

# Template specific dicts
_FAQ = {
    'FAQ_HEADER': "%(shorthand)s FAQ" % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'LOG_IN_WHAT_NOW_ANS_1': 'You need to follow the add participant workflow. Click on the "Add Source & Survey" tab located at the top of the page.',
    'INFORMATION_IDENTIFY_ME': 'Can data describing my gut microbiome be used to identify me or a medical condition I have?',
    'LOG_IN_WHAT_NOW_ANS_3': 'You can log a sample by clicking the "Associate Sample" link in the menu. If you do not see the "Associate Sample" link, then all of your barcodes have been assigned.',
    'PARTICIPATE_WITH_DIAGNOSIS': 'Can I participate in the project if I am diagnosed with ...?',
    'LOG_IN_WHAT_NOW_ANS_5': 'When adding a sample, please be sure to select the barcodes that matches the barcode on the sampling tube of the sample that you are logging',
    'TAKES_SIX_MONTHS': 'Does it really take up to three months to get my results?',
    'HOW_CHANGE_GUT': 'How can I change my gut microbiome?',
    'BETTER_OR_WORSE': 'How can I tell if my gut microbiome is better or worse than other people in my category?',
    'ONLY_FECAL_RESULTS_ANS': 'We have only sent out results for fecal samples and are in the process of evaluating how best to present the other sample types. Please see <a href="#faq12">the previous question </a>',
    'DIFFERENT_WHATS_WRONG_WITH_ME_ANS': 'No! Your gut microbiome is as unique as your fingerprint so you should expect to see some differences. Many factors can affect your gut microbiome, and any differences you see are likely to be the result of one of these factors. Maybe your diet is different than most people your age. Maybe you just traveled somewhere exotic. Different does not necessarily mean bad.',
    'WHEN_RESULTS_NON_FECAL_ANS': 'The vast majority of the samples we\'ve received are fecal, which was why we prioritized those samples. Much of the analysis and results infrastructure we\'ve put in place is applicable to other sample types, but we do still need to assess what specific representations of the data make the most sense to return to participants. We apologize for the delay.',
    'FIND_DETAILED_INFO': 'Where can I find more detailed information about my sample?',
    'ADD_PARTICIPANT': '<a href="%(add_participant_vid)s">%(shorthand)s - How to Add a Participant</a> from <a href="http://vimeo.com/user16100300">shelley schlender</a> on <a href="http://vimeo.com">Vimeo</a>.' % {"shorthand": AMGUT_CONFIG.project_shorthand, 'add_participant_vid': media_locale["ADD_PARTICIPANT"]},
    'PASSWORD_DOESNT_WORK': "My password doesn't work!",
    'COMBINE_RESULTS': 'My whole family participated, can we combine the results somehow?',
    'PASSWORD_DOESNT_WORK_ANS': '<p>The passwords have some ambiguous characters in them, so we have this guide to help you decipher which characters are in your password.</p>'
                                '<p class="ambig">abcdefghijklmnopqrstuvwxyz<br>ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>1234567890<br>1 = the number 1<br>l = the letter l as in Lima<br>0 = the number 0<br>O = the letter O as in Oscar<br>g = the letter g as in golf<br>q = the letter q as in quebec</p>',
    'HANDLING_SWABS': '%(shorthand)s - Handling Your SWABS</a> from' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'LOG_IN_WHAT_NOW_ANS_4': 'The generic add sample page looks like this:',
    'RAW_DATA_ANS_2': 'Processed sequence data and open-access descriptions of the bioinformatic processing can be found at our <a href="https://github.com/qiime/American-Gut">Github repository</a>.</p>'
                                '<p>Sequencing of %(shorthand)s samples is an on-going project, as are the bioinformatic analyses. These resources will be updated as more information is added and as more open-access descriptions are finalized.' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'RAW_DATA_ANS_1': '<P>The raw data can be fetched from the <a href=http://www.ebi.ac.uk/>European Bioinformatics Institute</a>. EBI is part of <a href=http://www.insdc.org/>The International Nucleotide Sequence Database Collaboration</a> and is a public warehouse for sequence data. The deposited %(project)s accession is <a href="http://www.ebi.ac.uk/ena/data/view/ERP012803&display=html">ERP012803</a>.' % {"project": AMGUT_CONFIG.project_name},
    'BETTER_OR_WORSE_ANS': 'Right now, you can\'t. We\'re still trying to understand what constitutes a normal or average gut microbiome, and we have a lot to learn about the functions of many of the microbes that inhabit the gut. Therefore, it\'s tough to know what combinations of microbes are best for nutrition and health. That\'s one reason collecting data from so many people is important - hopefully we can start to learn more about this.',
    'LOOK_BELOW': "If you're still experiencing issues, look for your problem in the FAQ below",
    'PASSWORD_SAME_VERIFICATION_ANS': 'No. Your <strong>password</strong> is printed on the sheet that you received with your kit in the mail. That sheet looks like this:</p>'
                                      '<img src="%(FAQ_AMBIGUOUS_PASS)s"/><p>Your <strong>verification code</strong> is emailed to you. Look for the email: <br /><br /><strong>FROM:</strong>  %(project)s (%(help_email)s)<br /><strong>SUBJECT:</strong>  %(shorthand)s Kit ID & Verification Code' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name, "FAQ_AMBIGUOUS_PASS": media_locale['FAQ_AMBIGUOUS_PASS'], 'help_email': media_locale['HELP_EMAIL']},
    'TAKES_SIX_MONTHS_ANS': 'Yes. It takes about eight weeks for extractions, eight weeks for the remainder of the processing, and two weeks to do the actual sequencing. This is before any analysis and if everything goes as planned, with no delays - equipment down, run failures, reagents or other consumables back ordered. Things do sometimes go wrong, so we say up to three months.',
    'PARTICIPATE_WITH_DIAGNOSIS_ANS': 'Of course! The only exclusion criteria are: you must be more than 3 months old and cannot be in prison. Please keep in mind that, for legal and ethical reasons, the %(project)s does not provide medically actionable results or advice.' % {"project": AMGUT_CONFIG.project_name},
    'HOW_PROCESS_SAMPLES': 'How are the samples and data processed?',
    'WHO_MICHAEL_POLLAN_ANS': 'Michael Pollan is a New York Times Best Seller for his books on diet and nutrition. Further information about Michael can be found <a href="http://michaelpollan.com/">here</a>.',
    'WHO_MICHAEL_POLLAN': 'Who is Michael Pollan?',
    'HOW_CHANGE_GUT_ANS': 'Although we still don\'t have a predictable way to change the gut microbiome in terms of increasing or decreasing the abundances of specific bacteria, we do know that a variety of factors influence gut microbial community composition. Diet is a major factor affecting the gut microbiome so by changing your diet, you may be able to affect your gut microbiome. We still don\'t fully understand probiotics but know that they can influence your gut microbiome while you are actively taking them. Factors such as stress can also influence the gut microbiome. However, it is important to remember that there are factors we can\'t change, such as age or genetics, that can affect the gut microbiome.',
    'RAW_DATA': 'How can I get the raw data?',
    'WATCH_VIDEOS': "Watch these helpful videos about what to do once you've received your kit!",
    'INTRODUCTION_BEGINNING': '<a href="http://www.robrdunn.com">Rob Dunn</a> has provided this excellent introduction to some of the basics that every curious reader should check out!<br/>&nbsp;<br/>Rob is the author of the <a href="http://www.yourwildlife.org/the-wild-life-of-our-bodies/">Wild Life of Our Bodies</a>. He is an evolutionary biologist and writer at North Carolina State University. For more about your gut and all of your other parts, read more from Rob at <a href="http://www.robrdunn.com">www.robrdunn.com</a></p>'
                                '',
    'INFORMATION_IDENTIFY_ME_ANS': 'No. First, all of your personal information has been de-identified in our database as mandated by institutional guidelines. Second, although each person has a unique gut microbiome, many of the unique qualities are at the species or strain level of bacteria. Our sequencing methods currently do not allow us to describe your gut microbiome in that much detail. Finally, for most medical conditions, there are no known, predictable patterns in gut microbial community composition. Research simply hasn\'t gotten that far yet.</p>'
                                '<p>We should also mention that since we are only interested in your microbes, we do not sequence human genomic DNA in our typical analyses. Where it is possible for human DNA to be sequenced (e.g., the Beyond Bacteria kits), we remove the human DNA using the same bioinformatics approaches undertaken in the NIH-funded Human Microbiome Project and approved by NIH bioethicists. Additionally, there is so little human DNA in fecal, skin and mucus samples that the chances of us being able to sequence your entire human genome are almost none, even if we tried.',
    'FECAL_NO_RESULTS_ANS': 'On any given sequencing run (not just the %(shorthand)s), a small percentage of the samples fail for unknown reasons -- our methods are good but not perfect. This is one of the reasons the sample kits have two Q-tips. It allows us to perform a second microbial DNA extraction and re-sequence if the first attempt failed. We will be doing this for all of the samples that failed. If there was a technical problem with the sample itself (e.g. not enough microbes on the swab) that inhibits us from producing data for you, we will be re-contacting you about collecting another sample.' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'MULTIPLE_KITS_DIFFERENT_TIMES_ANS': 'For best results, we recommend that you mail each sample within 24 hours of collection.',
    'STEPS_TO_FOLLOW': '<a href="%(video)s">%(shorthand)s - Steps to Follow When Your Kit Arrives</a> from <a href="http://vimeo.com/user16100300">shelley schlender</a> on <a href="http://vimeo.com">Vimeo</a>.' % {"shorthand": AMGUT_CONFIG.project_shorthand, "video": media_locale["STEPS_VIDEO"]},
    'WHY_TWO_SWABS': 'Why are there 2 swabs inside the tube?',
    'MULTIPLE_KITS_DIFFERENT_TIMES': 'I have a 2+ sample kit, and would like to collect and send them in at different times',
    'COMBINE_RESULTS_ANS': "We're still evaluating how best to present the data for samples that represent a family. We are mailing individual results now and will provide updated results through the web site later.",
    'PASSWORD_SAME_VERIFICATION': 'Is my password the same as my verification code?',
    'FECAL_NO_RESULTS': 'I sent in a fecal sample but did not get any results, what happened to them?',
    'DIFFERENT_WHATS_WRONG_WITH_ME': "I'm different than other people in my category. Does that mean something is wrong with me?",
    'WHY_TWO_SWABS_ANS_2': "<P>Each tube is used for <strong>one sample</strong>. The tube has two swabs in it because one is a backup in case the DNA does not amplify on the first swab.</p>"
                           "<p>Here's a video of Rob Knight talking about swab handling:</p>"
                           "<iframe src='%(swab_handling)s' width=''500'' height=''281'' frameborder=''0'' webkitallowfullscreen='' mozallowfullscreen='' allowfullscreen=''></iframe>" % {'swab_handling': media_locale['SWAB_HANDLING']},
    'MISSING_METADATA_ANS': 'Metadata are information describing your age, gender, diet, etc. Missing metadata mean that this person did not provide us with this information.',
    'WHERE_SEND_SAMPLE': 'Where do I send my sample?',
    'LOG_IN_WHAT_NOW': "I'm logged in, what do I do now?",
    'LOG_IN_WHAT_NOW_ANS_2': '<p>During this workflow you (or whomever is being sampled) will:</p>'
                                '<ol>   <li>Add a participant</li><li>Provide electronic consent</li><li>Answer survey questions (including the diet questions)</li><li>Upon completion, become eligible to associate samples</li>          </ol><p>When participants are eligible,  you will then see their name under the corresponding menu on the left, in this example we have just added the participant "Test":</p>'
                                '',
    'PROJECT_101': '%(shorthand)s 101' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'WHAT_FORMS_ANS': 'The instruction on the sampling instructions that requires you to "place your forms and the sample tube in preaddressed envelope" is leftover from a previous version of the sampling instructions. There are no forms for you to include inside the envelope with your sample. If you are shipping internationally, please visit the <a href="%(sitebase)s/international_shipping/">International Shipping Instructions</a></p>' % {'sitebase': media_locale['SITEBASE']},
    'WHY_TWO_SWABS_ANS_1': 'Each sampling tube contains two swabs and looks like this:',
    'MISSING_METADATA': 'What are missing metadata?',
    'ONLY_FECAL_RESULTS': 'I sent more than one kind of sample, but I only received data for my fecal sample. What happened to my other samples?',
    'NOT_A_BUSINESS_ANS': 'We have had many inquiries about our "service" or "business". %(shorthand)s is a contribution-supported academic project that is a collaboration between the <a href="http://www.earthmicrobiome.org">Earth Microbiome Project</a> and the <a href="http://humanfoodproject.com/">Human Food Project</a>, primarily run out of the <a href="https://knightlab.ucsd.edu/">Knight Lab</a> at the University of California San Diego, and is not a business or service.  In particular, %(shorthand)s is not a diagnostic test (although the information gained through the project may in future contribute to the development of diagnostic tests). All data except for information that needs to be kept confidential for privacy reasons is openly and freely released into public databases, and the project is not intended to make a profit (any surplus funds would be recycled back into furthering human microbiome research).' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'HOW_PROCESS_SAMPLES_ANS_1': 'The majority of the samples in the %(project)s are run through a processing pipeline designed to amplify a small region of a gene that is believed to be common to all Bacteria and Archaea. This gene, the 16S ribosomal RNA gene is like a barcode you find on your groceries, and serves as a marker for different organisms. There are quite a few different ways to assess the types of Bacteria and Archaea in a sample, including a variety of techniques even to look at this single gene. Every method has its biases, and comparing data between different methods is <a href="http://www.ncbi.nlm.nih.gov/pubmed/23861384">non-trivial</a> and can sometimes be nearly impossible. One of the primary goals of the %(shorthand)s is to provide data that can be used and reused by researchers worldwide, we have opted to use the standard protocols adopted by the <a href="http://earthmicrobiome.org">Earth Microbiome Project</a>, (<a href="http://www.ncbi.nlm.nih.gov/pubmed/22402401">Caporaso et al 2012</a>, and more detailed description of the <a href="http://www.earthmicrobiome.org/emp-standard-protocols/16s/">protocol</a>). This ensures that the data generated by the %(shorthand)s can be combined with the other 80,000 samples so far indexed by the EMP (as scientists, we get giddy about things like this).</p>' % {'shorthand': AMGUT_CONFIG.project_shorthand, 'project': AMGUT_CONFIG.project_name},
    'HOW_PROCESS_SAMPLES_ANS_2': 'DNA sequencing is a complex challenge that involves an army of robots, ultra pure water that costs $75 per 10ml, and an amazing <a href="http://www.illumina.com/systems/miseq.ilmn">digital camera</a> that actually determines individual sequences one nucleotide at a time. The number of stunningly brilliant minds whose footprints exist in these methods is astounding. However, the challenges don\'t end once you get the DNA sequence - some might say they are just beginning. It turns out that figuring out what actually is in your sample, that is, what organisms these sequences correspond to, requires cutting edge computational approaches, supercomputers and caffeine for the people operating them. The questions being asked of the data are themselves complex, and volume of data being processed is simply phenomenal. To give you some idea, for each sample sequenced we obtain around 6 million nucleotides which we represent as letters (A, T, G or C, see <a href="http://en.wikipedia.org/wiki/Nucleotide">here</a> for more info), whereas Shakespeare\'s Hamlet only contains around 150,000 letters (ignoring spaces).</p>',
    'HOW_PROCESS_SAMPLES_ANS_3': 'The primary software package we use for processing 16S sequence data is called Quantitative Insights into Microbial Ecology (<a href="http://www.qiime.org">QIIME</a>; <a href="http://www.ncbi.nlm.nih.gov/pubmed/20383131">Caporaso et al. 2010</a>). Using this package, we are able to start with raw sequence data and process it to so that we end up be able to  explore the relationships within and between samples using a variety of statistical methods and metrics. To help in the process, we leverage a standard and comprehensive (to date) reference database called Greengenes (<a href="http://www.ncbi.nlm.nih.gov/pubmed/22134646">McDonald  et al. 2011</a>; <a href="http://www.ncbi.nlm.nih.gov/pubmed/16820507">DeSantis et al. 2006</a>) that includes information on a few hundred thousand Bacteria and Archaea (it is likely that there are millions or more species of bacteria). Due to the molecular limitations of our approach, and the lack of a complete reference database (because the total diversity of microbes on Earth is still unknown), our ability to determine whether a specific organism is present has a margin of error on the order of millions of years, which limits our ability to assess specific strains or even species using this inexpensive technique (more expensive techniques, such as some of the higher-level analyses and contributions, can provide this information). But all is not lost! By using the evolutionary history of the organisms as inferred by the small pieces of DNA that we have, we can begin to ask broad questions about the diversity within (see <a href="http://www.ncbi.nlm.nih.gov/pubmed/7972354">Faith 1994</a>) and between samples (see <a href="http://www.ncbi.nlm.nih.gov/pubmed/16332807">Lozupone and Knight 2005</a>), and whether the patterns observed relate to study variables (e.g., BMI, exercise frequency, etc).</p>',
    'HOW_PROCESS_SAMPLES_ANS_4': 'The specifics on how the %(shorthand)s sequence data are processed can be found <a href="http://nbviewer.ipython.org/github/biocore/American-Gut/blob/master/ipynb/module2_v1.0.ipynb">here</a>, and are written up in an executable <a href="http://ipython.org/notebook">IPython Notebook</a>, which provides all the relevant processing steps in an open-source format. Be warned, processing the full %(shorthand)s dataset takes over 5,000 CPU hours right now (i.e. if you do it on your laptop it might take 7 months, even if you don\'t run out of memory: this might put the time it takes to get your results in perspective). This is the processing pipeline that we use on your data. As this project is a work in progress, we are versioning the processing pipeline as there will continue to be improvements to the process as the project moves forward.</p>' % {'shorthand': AMGUT_CONFIG.project_shorthand},
    'HOW_PROCESS_SAMPLES_ANS_5': 'Additional information about the tools used in the %(project)s and our contributions to the microbiome community can be found in the following publications:',
    'HOW_PROCESS_SAMPLES_ANS_6': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21552244">Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24280061">EMPeror: a tool for visualizing high-throughput microbial community data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16332807">UniFrac: a new phylogenetic method for comparing microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16893466">UniFrac--an online tool for comparing microbial community diversity in a phylogenetic context.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17220268">Quantitative and qualitative beta diversity measures lead to different insights into factors that structure microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/19710709">Fast UniFrac: facilitating high-throughput phylogenetic analyses of microbial communities including analysis of pyrosequencing and PhyloChip data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20827291">UniFrac: an effective distance metric for microbial community comparison.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21885731">Linking long-term dietary patterns with gut microbial enterotypes.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23326225">A guide to enterotypes across the human body: meta-analysis of microbial community structures in human microbiome datasets.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699609">Structure, function and diversity of the healthy human microbiome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699610">A framework for human microbiome research.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23587224">The Biological Observation Matrix (BIOM) format or: how I learned to stop worrying and love the ome-ome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22134646">An improved Greengenes taxonomy with explicit ranks for ecological and evolutionary analyses of bacteria and archaea.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304728">The Earth Microbiome Project: Meeting report of the "1 EMP meeting on sample selection and acquisition" at Argonne National Laboratory October 6 2010.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304727">Meeting report: the terabase metagenomics workshop and the vision of an Earth microbiome project.</a></li> </ul>',
    'HOW_PROCESS_SAMPLES_ANS_7': 'More detail on our work on the effects of storage conditions can be found in these publications:',
    'HOW_PROCESS_SAMPLES_ANS_8': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20412303">Effect of storage conditions on the assessment of bacterial community structure in soil and human-associated samples.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20673359">Sampling and pyrosequencing methods for characterizing bacterial communities in the human gut using 16S sequence tags.</a></li> </ul>',
    'HOW_PROCESS_SAMPLES_ANS_9': 'And more detail on our work on sequencing and data analysis protocols can be found in these publications:',
    'HOW_PROCESS_SAMPLES_ANS_10': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17881377">Short pyrosequencing reads suffice for accurate microbial community analysis.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18723574">Accurate taxonomy assignments from 16S rRNA sequences produced by highly parallel pyrosequencers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18264105">Error-correcting barcoded primers for pyrosequencing hundreds of samples in multiplex.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22237546">Selection of primers for optimal taxonomic classification of environmental 16S rRNA gene sequences.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22170427">Comparison of Illumina paired-end and single-direction sequencing for microbial 16S rRNA gene amplicon surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21716311">Impact of training sets on classification of high-throughput bacterial 16s rRNA gene surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21349862">PrimerProspector: de novo design and taxonomic analysis of barcoded polymerase chain reaction primers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20383131">QIIME allows analysis of high-throughput community sequencing data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22161565">Using QIIME to analyze 16S rRNA gene sequences from microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23861384">Meta-analyses of studies of the human microbiota.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24060131">Advancing our understanding of the human microbiome using QIIME.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20534432">Global patterns of 16S rRNA diversity at a depth of millions of sequences per sample.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22402401">Ultra-high-throughput microbial community analysis on the Illumina HiSeq and MiSeq platforms.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23202435">Quality-filtering vastly improves diversity estimates from Illumina amplicon sequencing.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699611">Human gut microbiome viewed across age and geography.</a></li> </ul>' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name},
    'ANOTHER_COPY_RESULTS_ANS': 'You can download a copy from our website. Log in with your account name and password, go to the left side bar, move your mouse to Human Samples -> PARTICIPANT NAME -> SAMPLE NUMBER, and then click on SAMPLE NUMBER.pdf to download it.' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name},
    'FIND_DETAILED_INFO_ANS': 'You can find the raw data from European Bioinformatics Institute (please see <a href="#faq8">here</a>) or download the copy of your result from our website (please see <a href="#faq20">here</a>).',
    'WHEN_RESULTS_NON_FECAL': 'I sent in a non-fecal sample and have not received any results, when should I expect results?',
    'WHAT_FORMS': 'What are the forms you talk about on the sampling instructions?',
    'INTRODUCTION_WHAT_IS_GUT_HEAD': "What is a Gut?",
    'INTRODUCTION_WHAT_IS_GUT': "Your gut is a hole that runs through your body. Your gut is actually, developmentally speaking, the outside of your body, but it has evolved many intricacies that make it seem like the inside. Your gut starts with your mouth and ends with your anus. In between food is changed into energy, feces, bacteria, viruses and a few other things. Your gut exacts a kind of metamorphosis on everything you eat, turning hotdog or grilled cheese, miraculously, into energy and, ultimately, cells, signals and even thoughts. We are only beginning to understand this process, a process in which microbes play (or fail to play) a major role.",
    'INTRODUCTION_WHAT_IS_PROJECT_HEAD': "What is the %(project_name)s?" % {'project_name': AMGUT_CONFIG.project_name},
    'INTRODUCTION_WHAT_IS_PROJECT': "<p>The %(project_name)s is a project in which scientists aim to work with non-scientists both to help them (AKA, you) understand the life inside their own guts and to do science. Science is coolest when it is informs our daily lives and what could possibly be more daily than what goes on in your gut? One of the big questions the %(project_shorthand)s scientists hope to figure out is what characterizes healthy and sick guts (or even just healthier and sicker guts) and how one might move from the latter to the former. Such is the sort of big lofty goal these scientists dream about at night (spirochetes rather than sugarplums dancing through their heads), but even the more ordinary goals are exciting. Even just beginning to know how many and which species live in our guts will be exciting, particularly since most of these species have never been studied, which is to say there are almost certainly new species inside you, though until you sample yourself (and all the steps that it takes to look at a sample happen&mdash; the robots, the swirling, the head scratching, the organizing of massive datasets), we won't know which ones. Not many people get to go to the rainforest to search for, much less discover, a new kind of monkey, but a new kind of bacteria, well, it is within (your toilet paper's) reach." % {'project_shorthand': AMGUT_CONFIG.project_shorthand, 'project_name': AMGUT_CONFIG.project_name},
    'INTRODUCTION_WHAT_IS_16S_HEAD': "What is 16S rRNA?",
    'INTRODUCTION_WHAT_IS_16S': "16S rRNA is a sort of telescope through which we see species that would otherwise be invisible. Let me explain. Historically, microbiologists studied bacteria and other microscopic species by figuring out what they ate and growing them, on petri dishes, in labs, in huge piles and stacks. On the basis of this approach&mdash; which required great skill and patience&mdash; thousands, perhaps hundreds of thousands, of studies were done. But then&hellip; in the 1960s, biologists including the wonderful radical <a href=\"http://www.robrdunn.com/2012/12/chapter-8-grafting-the-tree-of-life/\">Carl Woese</a>, began to wonder if the RNA and DNA of microbes could be used to study features of their biology. The work of Woese and others led to the study of the evolutionary biology of microbes but it also eventually led to the realization that most of the microbes around us were not culturable&mdash; we didn't know what they ate or what conditions they needed. This situation persists. No one knows how to grow the vast majority of kinds of organisms living on your body and so the only way to even know they are there is to look at their RNA. There are many bits of RNA and DNA that one might look at, but a bit called 16S has proven particularly useful.",
    'INTRODUCTION_ROBOTS_HEAD': "Do you really have a robot?",
    'INTRODUCTION_ROBOTS': "Look, here is the deal. Robots. Microbiologists use robots. Personally, I think the fact that microbiologists study the dominant fraction of life on Earth, a fraction that carries out most of the important process (and a fair bit of inexplicable magic) makes microbiologists cool. I am not a microbiologist; I am an evolutionary biologist and a writer, but I think that microbiologists are hipsters cloaked in scientists clothing (and language). But if the outrageousness of their quarry does not convince you they are hip, well, then, let me remind you, they have robots.<br/>&nbsp;<br/>The robots enable the scientists to rapidly extract the DNA and RNA from thousands of samples simultaneously. Specifically, they can load your samples into small plastic plates each with 96 little wells. The robot then loads chemicals into the wells and heats the chemically-laced wells enough to break open the bacterial cells in the sample, BAM! This releases the cell's DNA and RNA. The robots then decode the specific letters (nucleotides) of the 16S gene using the nucleotides dumped out of the broken microbial cells into these plates.",
    'INTRODUCTION_TREE_HEAD': "Tree of life",
    'INTRODUCTION_TREE': "There is an evolutionary tree inside you. Well, sort of. When scientists study the microbes in your gut (and from the same samples we could also study viruses, bacteriophages&mdash; the viruses that attack bacteria&mdash;, fungi or even the presence of animals such as worms of various sorts) they do so by looking at the 16s or other genetic code of the RNA on the swabs you send us. We compare the code of each bit of RNA we find to the code of species other people have collected and also the code of the other bits of RNA in your sample. As a result, we can actually use the results of your sample to map the species living in you onto an evolutionary tree. Your own genes occupy one tiny branch on the tree of life, but the species inside of you come from all over the evolutionary tree. In fact, in some people we find species from each of the major branches of the tree of life (archaea, bacteria, eukaryotes) and then also many of the smaller branches. Inside you, in other words, are the consequences of many different and ancient evolutionary stories.",
    'INTRODUCTION_MICROBIOME_HEAD': "What is a microbiome?",
    'INTRODUCTION_MICROBIOME': "A biome, as ecologists and evolutionary biologists like me historically used it is a self-contained ecosystem, where all the organisms can interact with each other and the environment in which they live, for example a rain forest is a biome, but it is made of smaller biomes, for example a tree is a biome for insects, then a single insect is a biome for bacteria. Therefore, these smaller biomes are often called microbiomes, in the case of you, it's your gut!&hellip; A microbiome is a small (micro) version of this larger phenomenon, a whole world within you.",
    'INTRODUCTION_EAT_HEAD': "What do my microbes eat?",
    'INTRODUCTION_EAT': "Everyplace you have ever set your hand or any other part of your body is covered in microbes. This is true of your gut, but also everything else. Microbes live in clouds. They live in ice. They live deep in the Earth. They also live in your colon, on your skin, and so on. It is reasonable to wonder what they eat. The short answer is everything. Microbes are thousands of times more variable when it comes to their diets than are animals, plants or even fungi. Some microbes can get their nitrogen out of the air; they can, in other words, eat air. Ain't that cool. Others, like us, eat other species, munching them in the world's coolest and most ubiquitous game of packman. The bacteria in your gut are also diverse in terms of their diets. If there are two hundred species of bacteria in your gut (and there probably are at least that many) then there are at least that many different combinations of things that they are eating.",
    'INTRODUCTION_MICROBES_COME_FROM_HEAD': "Where do my microbes come from?",
    'INTRODUCTION_MICROBES_COME_FROM': "If you had asked this question a few years ago, we would have had to say the stork. But increasingly we are beginning to understand more about where the specific zoo of species in you come from and it is a little grosser than the stork. If you were born vaginally, some of your gut microbes came from your mother's feces (birth, my friend, is messy). Some came from her vagina. Others came, if you were breast fed, from her milk. It is easiest for bacteria, it seems, to colonize our guts in the first moments of life. As we age, our stomachs become acidic. We tend to think of the acid of our stomachs as aiding in digestion; it does that but another key role of our stomachs is to prevent pathogenic species from getting into our guts. The trouble with this, well, there are a couple of problems. One is c-section birth. During c-section birth, microbes need to come from somewhere other than the mother's vagina and feces. The most readily available microbes tend to be those in the hospital. As a result, the microbes in c-section babies tend to, at least initially, resemble those of the hospital more than they resemble those of other babies. With time, many c-section babies eventually get colonized by enough good bacteria (from pet dogs, pet cats, their parents' dirty hands, etc..) to get good microbes, but it is a more chancy process. But then, the big question, one we just don't know the answer to, is which and how many microbes colonize our guts as we get older. How many microbes ride through the acid bath of our stomach on our food and take up residence? We know that bad bacteria, pathogens, do this, but just how often and how good ones do it is not well worked out. You might be thinking, what about yoghurt and I'll tell you the answer, definitely, is we don't really know. Do people who eat yoghurt have guts colonized by species from that yoghurt? Maybe, possibly, I bet they do, but we don't really know (though if we get enough samples from yoghurt and non yoghurt eaters, we could know).",
    'INTRODUCTION_DISCOVER_HEAD': "What will we discover in your gut?",
    'INTRODUCTION_DISCOVER': "When the early meetings were going on about this project, everyone sat around talking about what we might see from colon samples. One scientist was sure that we would see bacteria that looked like Elvis. Another though we would find Shakespeare's great lost play. But the truth is all that we are going to see from your gut are lists of nucleotides. Let me explain&hellip;<br/>&nbsp;<br/>Nucleotides are those hunks of protein out of which DNA and RNA are made. They come in different forms to which scientists have assigned names and letters. When the robots are done with the work, what they produce are lists of the nucleotides in all of 16S genes from all of the cells in your sample. These nucleotides tell the scientists which kinds of life are in your sample (and in you). But because we will only have samples of little stretches of the 16S genes, we won't know exactly which species are in you, just which lineages they are from. You might have the bacterial equivalent of a chimpanzee and a gorilla in you, but all we'll know from your sample is that there was an ape. Knowing you have a bacterial ape in your gut will, on its own, not tell you so much. The real information will come from context, statistical context. I know, that sounds boring, but I promise it is not.<br/>&nbsp;<br/>We think that hundreds of different things you do during your life, in addition to what your mother and father did (let's try not to think about that), your genes and even just where you grew up influence which species of microbes are found inside you. But we don't really know. The problem is humans are so darn complicated. What we need to be able to do is to compare large numbers of people, people who differ in many ways, to be able to sort out which variables are sometimes a little important and which ones are the big deal. Is a vegan gut very different from a vegetarian one? Does eating yoghurt make a big difference? Do the effects of a c-section birth last forever? These questions require us to compare many people, which is where you come in. Your sample, gives us context and it gives you context too. It won't be terribly exciting on its own (you will know which ancient lineages you have dividing and thriving inside you. OK, that is pretty cool on second thought), but it will be very exciting in context. Where do you fall relative to fish eaters, sick people healthy people, hunter gatherers, or even your dog? You will know and we will know. And this is not all.<br/>&nbsp;<br/>All of the questions I have mentioned so far are what I might call first order questions. How does this thing compare to that thing. But what we'd love to be able to answer are second order questions, contingent questions, questions such as whether the effect of your diet depends on your ethnicity (it probably does), whether the effect of having a dog depends on whether or not you live in the city (again, I bet it does) and so on. These questions are exactly the sort of question we have failed to be able to answer well when it comes to diet, because we don't have big enough samples sizes. We can see the forest for all of humans. Well, that isn't quite right, but you get the idea, we will be able to understand elaborate effects of multiple variables on the wilderness between your pie hole and the other hole and that, to us, is exciting.",
    'INTRODUCTION_STORIES_HEAD': "A few of the stories of the evolutionary tree in your gut",
    'INTRODUCTION_STORIES': "Some people have least favorite bacteria. Salmonella, for example, seems to have inspired some haters. But microbiologists also have favorite bacteria, as well they should. The stories of bacteria (and those who chase and study them) are among the most important of humanities stories and include the tales of many species without which we could not live, or whose presence or absence affects how we live. These species are as fascinating and, dare I say, lovely as pandas or koala bears, just harder to see and far more significant. I have begun to compile a book of the stories of some of the most common and interesting species you are likely to encounter&mdash; whether in your own gut, on your lettuce or the next time you sink your fingers into the soil. These stories will be available online here at <a href=\"http://invisiblelife.yourwildlife.org/\">Invisible Life</a> as they are compiled as a book, a book written by some of the very best science writers AND scientists out there. For starters, you might be interested to know that <a href=\"http://invisiblelife.yourwildlife.org/mycoplasma/\">the smallest species on Earth</a> is sometimes found inside humans and, once we look at your 16S, we will even know whether it lives in you. As more of these stories are written, they will appear here, eventually as an ebook, an ebook that you can reference when you find out what lives inside you to know whether your constant companion is a species we know everything about or, as is more typical, no one has ever studied. Like Charlie Chaplin once said&hellip; Wait, Charlie Chaplin was the one who didn't say anything wasn't he.",
    'ANOTHER_COPY_RESULTS': 'Can I get another copy of my results?',
    'NOT_A_BUSINESS': 'We are not a business',
    'WHERE_SEND_SAMPLE_ANS': '<p>This is the shipping address:</p>'
                              '%(address)s<p>If you are shipping internationally, please see the <a href="%(sitebase)s/international_shipping/">international shipping instructions</a>.' % {'sitebase': media_locale['SITEBASE'], 'address': media_locale['SHIPPING_ADDRESS']}
}


_TAXA_SUMMARY = {'RESOLUTION_NOTE': "Note: Where there are blanks in the table below, the taxonomy could not be resolved in finer detail.",
                 'PERCENTAGES_NOTE': "Note: The percentages listed represent the relative abundance of each taxon. This summary is based off of normalized data. Because of limitations in the way the samples are processed, we cannot reliably obtain species level resolution. As such, the data shown are collapsed at the genus level.",
                 'DOWNLOAD_LINK': "Download the table"}

_INTERACTIVE_MULTIPLE = {'TAXA_CHART_TEXT': 'You can explore the relative abundances of bacterial taxa found in your sample(s). The taxonomic levels that you can look at range from Phylum (shallow) to Genus (deep). An explanation of taxonomy and taxonomic levels can be read <a href="https://microbio.me/%(sitebase)sauthed/addendum/#taxcharts">here</a>; for an explanation of why 16S marker gene sequencing cannot identify species, please see <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1950982/">this paper</a>). If you look at deeper taxonomic levels, they will be colored different shades of the corresponding phylum color. Rolling over a color will tell you the bacterial taxonomy and relative abundance of that taxonomy in that sample. Clicking on a specific taxa of interest in the bar chart will show that taxa alone, expanded to the next lowest taxonomic level (i.e. clicking on a taxa at phylum level will expand it to the class level).  If you have more than one sample, they are all shown for easy comparison, and are ordered by collection date. You can remove any sample you don\'t want to visualize by clicking "Remove" below an individual sample label. You can also choose to add a bar specific to a body site (i.e., stool) and category (i.e., age group) so that you can compare your sample(s) to a defined set of all %(shorthand)s data.' % {'sitebase': _SITEBASE, 'shorthand': AMGUT_CONFIG.project_shorthand},
                         'COMP_CHART_TEXT': 'You can compare the bacteria (from Phylum to Genus level) we found in your sample to specific groups; for example, people in the same age group as you. The graph will show the direction of change for the taxa that are different between your sample and the comparison group you choose. For example, if you choose Class as the taxa level and age-20s as the category for  comparison, you will see several bars pointing up (increased in your sample compared to the comparison group) and down (decreased in your sample compared to the comparison group), and each bar will be labelled by bacterial Class. By default, we compare you with all samples of the same type, e.g. all stool if your sample is stool.',
                         'ALPHA_DIV_TEXT': 'This graph compares the alpha diversity in your sample to the alpha diversity from all samples at the same body site in %(shorthand)s. You can explore the diversity of your sample in relation to the diversity of a specific comparison group (i.e. age-20s). The black line represents your sample diversity, while the blue line represents the average diversity for the comparison group you chose (with the blue shading indicating where 68%% of the population typically falls).<br/><br/>Here you can see the alpha diversity of your sample. We are illustrating PD Whole Tree, which calculates the level of phylogenetic diversity in your sample. For example, two samples, each with 5 taxa, might be considered equally diverse (the number of taxa in each is the same). BUT-if one of those samples is only Bacteroides and the other contains a mix of Bacteroides, Prevotella, and Ruminococcus, the second sample is more phylogenetically diverse. For more information about alpha diversity, please see our two part blog post: <a href="http://americangut.org/using-my-thai-chili-experiment-to-describe-variability-of-diversity-part-1/">(1) <a href="http://americangut.org/using-my-thai-chili-experiment-to-describe-variability-of-diversity-part-2/">(2)</a>' % {'shorthand': AMGUT_CONFIG.project_shorthand},
                         'RESET_GRAPH': 'Reset graph',
                         'COMPARE_POP': 'Compare with population averages',
                         'EXPLORE_IN_DETAIL': 'Explore a sample in detail',
                         'CATEGORY': 'Category',
                         'SELECT_LEVEL': 'Select taxa level',
                         'PHYLUM': 'Phylum',
                         'CLASS': 'Class',
                         'ORDER': 'Order',
                         'FAMILY': 'Family',
                         'GENUS': 'Genus',
                         'ALPHA_DIVERSITY': 'Alpha Diversity',
                         'REL_TAXONOMY': 'Relative taxonomy',
                         'ADD_SITE': 'Add site',
                         'SKIN': 'skin',
                         'ORAL': 'oral',
                         'STOOL': 'stool',
                         'CATEGORY': 'category',
                         'ADD': 'Add',
                         'REMOVE': 'Remove',
                         'SAMPLE': 'Sample',
                         'TAX_REL_ABUNDANCES': 'Taxonomic Relative Abundances',
                         'PERCENT_ABUNDANCE': 'Percent abundance',
                         'TAX_FOLD_CHANGES': 'Taxonomic Fold Changes',
                         'LOG2_FOLD_CHANGE': 'Log2 Fold Change'
}

_INTERACTIVE_CATEGORIES = {
    'age-baby': 'age-baby',
    'age-child': 'age-child',
    'age-teen': 'age-teen',
    'age-20s': 'age-20s',
    'age-30s': 'age-30s',
    'age-40s': 'age-40s',
    'age-50s': 'age-50s',
    'age-60s': 'age-60s',
    'age-70+': 'age-70+',
    'bmi-Underweight': 'bmi-Underweight',
    'bmi-Normal': 'bmi-Normal',
    'bmi-Overweight': 'bmi-Overweight',
    'bmi-Obese': 'bmi-Obese',
    'sex-male': 'sex-male',
    'sex-female': 'sex-female',
    'diet-Omnivore': 'diet-Omnivore',
    'diet-Omnivore but do not eat red meat': 'diet-Omnivore but do not eat red meat',
    'diet-Vegetarian but eat seafood': 'diet-Vegetarian but eat seafood',
    'diet-Vegetarian': 'diet-Vegetarian',
    'diet-Vegan': 'diet-Vegan',
    'cosmetics-Daily': 'cosmetics-Daily',
    'cosmetics-Regularly': 'cosmetics-Regularly',
    'cosmetics-Occasionally': 'cosmetics-Occasionally',
    'cosmetics-Rarely': 'cosmetics-Rarely',
    'cosmetics-Never': 'cosmetics-Never',
    'flossing-Regularly': 'flossing-Regularly',
    'flossing-Occasionally': 'flossing-Occasionally',
    'flossing-Rarely': 'flossing-Rarely',
    'flossing-Never': 'flossing-Never'

}

_HELP_REQUEST = {
    'CONTACT_HEADER': "Contact the %(shorthand)s" % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'RESPONSE_TIMING': "We will send a response to the email address you supply within 24 hours.",
    'FIRST_NAME': "First name",
    'LAST_NAME': "Last name",
    'EMAIL_ADDRESS': "Email address",
    'PROBLEM_PROMPT': "Enter information related to your problem"
}

_DB_ERROR = {
    'HEADER': 'Oops! There seems to be a database error.',
    'MESSAGE': 'Please help us to debug by emailing us at <a href="mailto:%(help_email)s">%(help_email)s</a> and tell us exactly what happend before you got this error.' % {"help_email": media_locale["HELP_EMAIL"]},
    'SIGNOFF': 'Thanks, <br /> The American Gut Team'
}

_404 = {
    'MAIN_WARNING': '404: Page not found!',
    'HELP_TEXT': 'Click <a href="mailto:%(help_email)s">HERE</a> to email us about the issue. Please include the URL you were trying to access:' % {'help_email': media_locale['HELP_EMAIL']}
}

_403 = {
    'MAIN_WARNING': '403: Unauthorized access!',
    'HELP_TEXT': 'Click <a href="mailto:%(help_email)s">HERE</a> to email us about the issue. Please include the URL you were trying to access:' % {'help_email': media_locale['HELP_EMAIL']}
}

_PARTICIPANT_OVERVIEW = {
    'COMPLETED_CONSENT': 'Completed consent',
    'COMPLETED_SURVEY': 'Completed survey',
    'SAMPLES_ASSIGNED': 'Samples assigned',
    'OVERVIEW_FOR_PARTICPANT': 'Overview for participant',
    'VIOSCREEN_CONTINUE': '<a href="%s"><button>Continue your Food Frequency Questionnaire</button></a>',
    'VIOSCREEN_COMPLETE': 'Food Frequency Questionnaire completed',
    'VIOSCREEN_START': '<a href="%s"><button>Start the Food Frequency Questionnaire</button></a>'
}

_ADD_SAMPLE_OVERVIEW = {
    'ADD_SAMPLE_TITLE': 'Choose your sample source ',
    'ADD_SAMPLE_TITLE_HELP': 'The sample source is the person, animal or environment that the sample you are currently logging came from. If you took the sample from yourself, you should select yourself as the sample source.',
    'ENVIRONMENTAL': 'Environmental',
    'ADD_SAMPLE_1': 'If you don\'t see the sample source you want here, you need to add it. You can do this in ',
    'ADD_SAMPLE_2': 'Step 2',
    'ADD_SAMPLE_3': ' on the main page when you log in.',
    'HUMAN_SOURCE': 'Human Source',
    'ANIMAL_SOURCE': 'Animal Source'
}

_SAMPLE_OVERVIEW = {
    'BARCODE_RECEIVED': 'Sample %(barcode)s. This sample has been received by the sequencing center!',
    'DISPLAY_BARCODE': 'Sample %(barcode)s',
    'RESULTS_PDF_LINK': 'Click this link to visualize sample %(barcode)s in the context of other microbiomes!',
    'SAMPLE_NOT_PROCESSED': 'This sample has not yet been processed. Please check back later.',
    'DATA_VIS_TITLE': 'Data Visualization',
    'TAXA_SUM_TITLE': 'Taxa Summary',
    'RAW_SEQUENCE_TITLE': 'Raw sequences',
    'EXCEL_TABLE_TITLE': 'Summarized data',
    'BIOM_TABLE_TITLE': 'Summarized data (<a href="http://biom-format.org">biom-format.org</a>)',
    'VIEW_TAXA_SUMMARY': 'View Taxa Summary',
    'SAMPLE_STATUS': 'Sample Status',
    'SAMPLE_SITE': 'Sample Site',
    'SAMPLE_DATE': 'Sample Date',
    'SAMPLE_TIME': 'Sample Time',
    'SAMPLE_NOTES': 'Notes',
    'REMOVE_BARCODE': 'Remove barcode %(barcode)s',
    'DATA_NOT_AVAILABLE': 'These data are not available yet for download.',
    'sequence_url': 'Download FASTQ from EBI',
    'test': 'some test caption',
    'test2': 'some other test caption'
}

_NEW_PARTICIPANT_OVERVIEW = {
    'ADD_NEW': 'Add a New Human Sample Source',
    'EXPLANATION': 'You have entered the add human source workflow. During this workflow you will add a human source that represents whoever is being sampled. You be asked for consent to join the project and then asked survey questions.',
    'ONCE_ADDED': 'Once you have added a human source, you will then see the name of that source in the left menu, and you will also have an option for adding a sample to that source. When you click that, you will be able to select the appropriate barcode and add sample metadata.',
    'ELECTRONIC_SIGNATURE': 'In order to participate in this study, you will need to sign a research consent form. This must be done electronically. To consent to using an electronic signature, please click the button below. To obtain a hard copy of the signed agreement, please email the help desk (americangut@gmail.com). You may revoke this consent at any time by going to human samples -> person name -> remove person name. Revoking consent will also halt processing of your sample, if applicable. Once your sample is processed, we cannot remove it from the deidentified information distributed, regardless of consent revocation.',
    'ELECTRONIC_SIG_CONSENT': 'I consent to using an electronic signature'
}

_INTERNATIONAL = {
    'PAGE_TITLE': '%(shorthand)s International Shipping Instructions' % {'shorthand': AMGUT_CONFIG.project_shorthand},
    'INTERNATIONAL_HEADER_1': "International Shipping",
    'INTERNATIONAL_TEXT_1': 'Please send any non-UK international samples to:',
    'INTERNATIONAL_TEXT_2': 'In order to comply with amended federal and IATA regulations, we are requesting that international participants return their sample tubes through FedEx International and that international participants follow the additional safely requirements for shipping human swab samples to the United States. Your airway bill must clearly identify the package as containing "human exempt specimens". The samples will additionally need to be packaged within a secondary containment to ensure that they can safely enter the United States.',
    'INTERNATIONAL_TEXT_3': "For shipment, you will need to use clear tape to secure the sample swabs to the sample tube, then place the sample tube in the provided buff mailing envelope. Then place the buff envelope inside a Tyvek/plastic mailer, <strong>which can be acquired free of charge from FedEx</strong>, when shipping the sample, prior to FedEx shipment.",
    'INTERNATIONAL_TEXT_4': "If you do not follow these directions the sample will be destroyed by United States Customs at the port of entry into the United States.",
    'YOUR_SAMPLES': 'Your samples',
    'YOUR_SAMPLES_LIST': '<li>Are considered dried specimens</li><li>Must be shipped via FedEx</li><li>Must have tape to sealing the plastic tube that contains the swab</li><li>Must be placed in a buff mailing envelope with the buff envelope placed inside a Tyvek/plastic mailer prior to FedEx shipment</li><li>Must be shipped with an airway bill and must be labeled with the complete address of the sender and complete address of recipient, and with the words "Human exempt sample(s)"</li>',
    'AMERICAN_GUT_ADDRESS': media_locale["SHIPPING_ADDRESS"]
}

_NEW_PARTICIPANT = {
    'ADD_HUMAN_TITLE': 'Add a New Human Source',
    'SEL_AGE_RANGE': 'Select age range of participant:',
    'ADD_HUMAN_HELP_SUGGESTION': 'If you need help with the website, please use the contact mechanism in the menu to the left. Please do not email the people listed in this form for help, unless it has to do with an injury. ',
    'AGE_0_6': '3 months - 6 years',
    'AGE_7_12': '7-12 years',
    'AGE_13_17': '13-17 years',
    'AGE_18': '18+ years',
    'ASSENT_7_12': '''<p align='center'>University of California, San Diego<br/>
Assent to Act as a Research Subject<br/>
(Ages 7-12 years)</p>

<p align='center'><b>Human bugs: why and where they live on you</b></p>


<p>Dr Rob Knight and his research team are doing a research study to find out more about the trillions of  tiny living things likes bacteria that live in you or on you. You are being asked if you want to be in this study because you are different (in a good way) from everybody else and they are different from each other.</p>
<p>If you decide you want to be in this research study, this is what will happen to you:</p>
<p>We will ask you or your mom or dad to sample some place on your body (like skin or mouth) or your poop (from toilet paper) with something that looks like 2 Q-tips.</p>
<p>Sometimes kids don't feel good while being in this study. You might feel a little bit sore where your skin is rubbed with the Q-tip.  Most people don't feel this.</p>
<p>If you feel any of these things, or other things, be sure to tell your mom or dad.</p>
<p>You don't have to be in this research study if you don't want to. Nobody will be mad at you if you say no. Even if you say yes now and change your mind after you start doing this study, you can stop and no one will be mad.</p>
<p>Be sure to ask Dr. Knight or his research team to tell you more about anything you don't understand.</p>
''',
    'ASSENT_13_17':
    '''<p align='center'>University of California, San Diego<br/>
Assent to Act as a Research Subject<br/>
(Ages 13-17 years)</p>

<p align='center'><b>Explaining variability in the human microbiome</b></p>


<p style='font-weight: bold;'>Who is conducting the study, why you have been asked to participate, how you were selected, and what is the approximate number of participants in the study?</p>
<p>Professor Rob Knight is conducting a research study to find out more about the microbiome (harmless or beneficial microorganisms (tiny living things such as bacteria) that live on and within your body). You have been asked to participate in this study because you, and everyone else on earth have a unique microbiome, and the more people we study of all ages will help us to understand how the micro-organisms may help or harm us. There will be approximately 1000 participants in total.</p>

<p style='font-weight: bold;'>Why is this study being done?</p>
<p>The purpose of this study is to try to understand why different kinds of microorganisms live on and within different people. We are interested in learning whether people with similar age, diet, environment, family, pets, body weight, or other features, also have similar microorganisms. Investigating this question will help us determine how microorganisms contribute to human biology and human health.</p>

<p style='font-weight: bold;'>What will happen to you in this study and which procedures are standard of care and which are experimental?</p>
<p>If you agree to to take part in this study, the following will happen to you: You will be asked to sign this assent form and then complete a survey about what you eat, how old you, are, whether you are a boy or girl, how tall you are and how much you weigh.</p>
<p>Then you will be asked to sample yourself  with the swabs (look like Q-tips) we give you.  The most common sample is of your poop (stool) where you apply a small smear to the tips of the swab from used toilet tissue.  You may also sample any area of skin, your tongue or mouth, your nostrils, ear wax, vagina, hair or nails. The sampling is usually done by you at home or with the help of your mom or dad if it is in a hard to reach place.  We will ask you if you are willing to let us use what is left of your sample for other studies.</p>

<p style='font-weight: bold;'>None of these samples will allow us to make a diagnosis of disease.</p>
<p>We intend to look at the different types of bacteria in your sample by getting out their DNA - we won't take out any of your DNA.</p>

<p style='font-weight: bold;'>How much time will each study procedure take, what is your total time commitment, and how long will the study last?</p>
<p>It should take you about 30 minutes to answer the survey questions and less than 15 minutes each time we ask you for a sample.</p>

<p style='font-weight: bold;'>What risks are associated with this study?</p>
<p>It is unlikely that there are risks to you from taking part in the study.  The investigation staff have taken precautions to ensure that there is minimal risk of your private information leaking out.  If the information about you were to become public the impilications are minimal because the tests cannot be used for diagnosis.</p>

<p>Because this is a research study, there may be some unknown risks that are currently unforeseeable. You will be informed of any significant new findings.</p>

<p style='font-weight: bold;'>What are the alternatives to participating in this study?</p>
<p>You do not have to participate. No harm would come to you.</p>

<p style='font-weight: bold;'>What benefits can be reasonably expected?</p>
<p>There is no direct benefit to you from taking part in this study. The investigator may learn more about the human microbiome in health and disease and benefit everyone.</p>

<p style='font-weight: bold;'>Can you choose to not participate or withdraw from the study without penalty or loss of benefits?</p>
<p>Participation in research is entirely voluntary. You may refuse to participate or withdraw at any time without upsetting the researchers. You will be told if any important new information is found during the course of this study that may affect your wanting to continue.</p>

<p style='font-weight: bold;'>Can you be withdrawn from the study without your assent?</p>
<p>You may be withdrawn from if you do not sign this form. You may also be withdrawn from the study if you do not follow the instructions given you by the study personnel.</p>

<p style='font-weight: bold;'>Will you be compensated for participating in this study?</p>
<p>You will not be financially compensated in this study.</p>

<p style='font-weight: bold;'>What if you are injured as a direct result of being in this study?</p>
<p>If you are injured or become ill as a direct result of this research study, you will be provided with medical care.</p>

<p style='font-weight: bold;'>What about your confidentiality?</p>
<p>Research records will be kept confidential to the extent allowed by law. All data about you that is entered on the survey is stored on a password-protected server located at the SDSC card access controlled facility at UCSD. The code key (that records which barcode or sample name was on your sample) is stored on a separate password-protected server that is accessible only to Professor Knightand Dr Gail Ackermann.  All analysis is done on data that has no record of who you are.  We will put the data into a place where other reseachers can access it, but there will not be a way of determining who you are from what is in there.</p>

<p>Research records may be reviewed by the UCSD Institutional Review Board.</p>

<p style='font-weight: bold;'>Who can you call if you have questions?</p>
<p>Dr Rob Knight and/or Gail Ackermann has explained this study to you and answered your questions. If you have other questions or research-related problems, you may reach Dr Knight at 858-246-1184</p>

<p>You may call the Human Research Protections Program Office at (858) 246-7444 to inquire about your rights as a research subject or to report research-related problems.</p>

<p style='font-weight: bold;'>Your Signature and Assent</p>
<p>You have received a copy of this assent document and a copy of the "Experimental Subject's Bill of Rights" to keep.</p>

<p>You agree to participate.</p>''',
    'CONSENT_18':
        '''<p align='center'>University of California, San Diego<br/>
Consent to Act as a Research Subject</p>

<p style='font-weight: bold;' align='center'>American Gut Project</p>

<p style='font-weight: bold;'>Who is conducting the study, why you have been asked to participate, how you were selected, and what is the approximate number of participants in the study?</p>
<p>Dr Rob Knight is conducting a research study to find out more about the trillions of bacteria and other organisms (called your microbiome) that live in and on your body. You have been asked to participate in this study because your microbiome is unique - not the same as anyone else on earth. There will be approximately 20,000 participants in the study from across the USA and from other countries around the world.</p>

<p style='font-weight: bold;'>Why is this study being done?</p>
<p>The purpose of this study is to more accurately assess the differences between people and whether these differences can be attributable to lifestyle, diet, body type, age or the presence of associated diseases.  The results will be used to create a database of sequence data derived from bacterial DNA in various body sites (e.g. skin, mouth, gut) and details about the participant supplying the sample from these different people that can be used by other researchers when they need samples to compare to what they are studying e.g. certain diseases where gut abnormalities are common.</p>

<p style='font-weight: bold;'>What will happen to you in this study?</p>
<p>You are being asked if you want to be in this study because you signed up for microbial analysis on the American gut website. When you signed up we sent you a sample kit with instructions on how to login to the website so that you can consent to the study formally.</p>

<p>The level of analysis available to you will depend on your contribution but all participants will have to consent to be a part of the study.
The following tests are available:</p>
<ol>
<li>Find out who is in your microbiome - which bacteria and other microbes that are similar to bacteria called archaea are present in your child's sample ($99/swab kit);</li>
<li>You plus the world - This is two kits: 1 for your child and one for someone from Africa, South America or Asia. Your support of for the second sample will allow us to sequence more people from around the world as part of our ongoing research ($129/kit);</li>
<li>Microbes for two, three or four - which bacteria and other microbes that are similar to bacteria called archaea are present in your child's sample and one, two or three other samples;</li>
<li>A week of feces - seven stool swab samples to be used any way you want - to track the effects of an antibiotic on your gut, effect of foreign travel e.g. ($500/7sample kit);</li>
<li>All in the Family - Where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shallow shotgun metagenomic analysis") of up to four fecal samples with analysis of the pathways used by bacteria to signal other bacteria or within themselves;</li>
<li>Beyond Bacteria - Deeper shotgun metagenome and virome characterization (where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present making use of additional gene parts that can tell us if there are any associated viruses or virus products that "talk " with bacteria, fungus and parasites that may be present in the sample from your gut.  Requires shipment of a whole stool sample (materials and return FedEx postage included) ($2500/kit);</li>
<li>Functional Feces - Additional characterization of gut samples over time (up to 7 stool samples, providing an analysis of the variability of functions over time. Here too the DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shotgun metagenomic analysis").</li>
</ol>
<p>We will analyze all samples where the consent form and questionnaire is completed.  The samples in the project (including yours) will be analyzed and published as a scientific article defining the range of diversity in the human microbiome.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to a more detailed list of the different organisms present in your sample (taxonomy summary).</p>
<p>We would like you to understand from the consent what we will do with your sample and what you will get in return.</p>

<p>We will ask you to complete an online questionnaire about you your lifestyle and what you eat.  We estimate that this should take no more than 30 minutes. You will then sample a part of your body (of interest to you) with a sterile Q-tip like swab by rubbing the surface of your skin, rubbing the surface of your tongue or sampling your stool by inserting the tip of the swab into used toilet tissue.  You can also sample other parts of your body - ear, nose, vagina, scalp, sole of foot. The swabs should be returned to us in the envelope provided using regular US mail service. DNA will be extracted from the sample and amplified by PCR (polymerase chain reaction) and then sequenced to see what bacteria are present and in what proportion in your sample. We estimate that it will take 2 months for you to learn the results.</p>
<p>For the Beyond Bacteria package you will submit a whole stool sample in a designated collection device on special ice packs (that reliably cool the sample to -20 degrees celsius/-4 degrees Fahrenheit) in a container that we will provide.  The results for "Beyond Bacteria" and "All in the family" will take longer to analyze because more extensive analysis is provided.  Results will be uploaded to your American Gut account when they are available.  We are also asking you to consent to having your sample or the bacterial DNA from it to be used in future studies.</p>

<p style='font-weight: bold;'>Please Note: The sequencing is not for diagnostic purposes and does not target human DNA.

<p style='font-weight: bold;'>How much time will each study procedure take, what is your total time commitment, and how long will the study last?</p>
<p>To complete the online questionnaire should take 30 minutes or less.  Each sample you send can be obtained in 5 minutes or less.  We expect the study to continue for 5 years but your results will be available to you before the end of the study (usually within 2 months of us receiving the sample).  You can elect to sample yourself more than once. If your personal details change (e.g. address, or your heath status) we request that you voluntarily re-enter your responses to the questionnaire.</p>

<p style='font-weight: bold;'>What risks are associated with this study?</p>
<p>The sampling techniques have been used for ~5 years with no reported side effects. We do not target the human DNA that may be in the sample so personal information about your genome will not be available to us.  The investigation personnel have taken precautions to ensure that there is minimal risk of loss of confidentiality.  Should confidentiality be compromised, the implications to you are minimal since the results are not diagnostic and have no implications for insurance companies that could compromise your insurability.</p>
<p>Because this is a research study, there may be some unknown risks that are currently unforeseeable. You will be informed of any significant new findings.</p>

<p style='font-weight: bold;'>What are the alternatives to participating in this study?</p>
<p>The study is entirely voluntary and not participating will have no consequence.  There is no alternative test.</p>

<p style='font-weight: bold;'>What benefits can be reasonably expected?</p>
<p>There is no direct benefit to you for participating in this study. We believe that there may be natural curiosity to know what microbes are in your sample and how this compares to other people of the same gender and age. The investigator, however, will learn more about the human microbiome in health and disease and provide a valuable resource for other researchers in other studies.  Your contribution to the project may be eligible as a tax-deduction.  The receipt will be sent to you from the site that handles financial contributions.</p>

<p>We will analyze all samples where the consent form and questionnaire is completed.  The samples in the project (including yours) will be analyzed and published as a scientific article.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed taxa report of your results.</p>
<p>The results from analysis of your sample/s cannot be used by you or your doctor to confirm a clinical diagnosis and we are not testing for infectious disease.</p>

<p style='font-weight: bold;'>Can you choose to not participate or withdraw from the study without penalty or loss of benefits?</p>
<p>Participation in research is entirely voluntary. You may refuse to participate or withdraw at any time without penalty or loss of benefits to which you are entitled. If you decide that you no longer wish to continue in this study, you will be requested to contact the American Gut Project helpline to inform us of your intent to withdraw.  If your sample has not been processed you may request a refund which will be processed through the site where you contributed to the project.</p>
<p>You will be told if any important new information is found during the course of this study that may affect your wanting to continue.</p>

<p style='font-weight: bold;'>Can you be withdrawn from the study without your consent?</p>
<p>You may be withdrawn from the study if you do not complete the consent. You may also be withdrawn from the study if you do not follow the instructions given you by the study personnel.</p>

<p style='font-weight: bold;'>Will you be compensated for participating in this study?</p>
<p>You will not be financially compensated in this study.</p>

<p style='font-weight: bold;'>Are there any costs associated with participating in this study?</p>
<p>You will be asked to contribute money to the project commensurate with the investigation you request ($99 for one sample, $1500 for "All in the family" (shallow shotgun metagenomic sequencing) and $2500 for "Beyond Bacteria" (deeper shotgun metagenome and virome characterization of one sample, plus additional sequencing). A receipt will be sent to you after you pay for the analysis you are requesting.  These contributions are used to partially finance the project.  Any additional funds required are provided from the funds UCSD has provided to Dr. Knight to set up his laboratory.</p>

<p style='font-weight: bold;'>What if you are injured as a direct result of being in this study?</p>
<p>If you are injured as a direct result of participation in this research, the University of California will provide any medical care you need to treat those injuries. The University will not provide any other form of compensation to you if you are injured. You may call the Human Research Protections Program Office at (858) 246-7444 for more information about this, to inquire about your rights as a research subject or to report research-related problems.</p>

<p style='font-weight: bold;'>What about your confidentiality?</p>
<p>Research records will be kept confidential to the extent allowed by law. All data about you that is entered on the web site is stored on a password-protected server located at the SDSC (San Diego Supercomputer Center) card access controlled facility at UCSD.  Financial information from participants contributing to the project is not accessible to the researchers.  The code key (that relates participant personal information to sample barcodes) is retained on a separate password-protected server that is accessible only to the PI, Co-I, sample coordinator and the database coders.  All analysis is done on de-identified data and the data deposited in a public repository for use by other investigators, is similarly de-identified. Research records may be reviewed by the UCSD Institutional Review Board.</p>
<p>You will provide information about yourself that could allow you to be identified if it was made public e.g. name, age, birthdate, address.  We have made every effort to ensure that you cannot be identified from the data you supply about yourself but retaining critical information like gender, age without compromising your personal information or the data integrity.</p>

<p>We may need to report information about known or reasonably suspected incidents of abuse or neglect of a child, dependent adult or elder including physical, sexual, emotional, and financial abuse or neglect. The only way we could discover such abuse is if it is self-reported by the participant or the legal guardian, so this is not likely.  If any investigator has or is given such information, he or she may report such information to the appropriate authorities.</p>

<p style='font-weight: bold;'>Who can you call if you have questions?</p>
<p>If you have questions or research-related problems, you may reach Rob Knight at 858-246-1184 or contact Brent Erickson at 858-534-8739.</p>

<p>You may call the Human Research Protections Program Office at (858) 246-7444 to inquire about your rights as a research subject or to report research-related problems.</p>

<p style='font-weight: bold;'>Your Signature and Consent</p>
<p>You have received a copy of this consent document and a copy of the "Experimental Subject's Bill of Rights" to keep.</p>
<p>You agree to participate.</p>''',
    'CONSENT_YOUR_CHILD': '''<p align='center'>University of California, San Diego<br/>
Parent Consent for Child to Act as a Research Subject<br/></p>

<p align='center' style='font-weight: bold;'>American Gut Project</p>

<p style='font-weight: bold;'>Who is conducting the study, why your child been asked to participate, how your child was selected, and what is the approximate number of participants in the study?</p>
<p>Dr. Rob Knight is conducting a research study to find out more about the trillions of bacteria and other organisms (called the microbiome) that live in and on the body. You are volunteering your child for this study because you want to know more about the microbiome of your child. Children like all humans have a unique microbiome and including them in the study will help elucidate the development of the microbiome. There will be approximately 20,000 participants in the study from across the USA and from other countries around the world.</p>

<p style='font-weight: bold;'>Why is this study being done?</p>
<p>The purpose of this study is to more accurately assess the differences between people and whether these differences can be attributable to lifestyle, diet, body type, age or the presence of associated diseases.  The results will be used to create a database of sequence data derived from bacterial DNA in various body sites (e.g. skin, mouth, gut) and details about the child participant supplying the sample  that can be used by other researchers when they need samples to compare to what they are studying e.g. certain diseases where gut abnormalities are common.</p>

<p style='font-weight: bold;'>What will happen to your child in this study and which procedures are standard of care and which are experimental?</p>
<p>You are being asked if you want your child to be in this study because you signed up for microbial testing on the American gut website. When you signed up we sent you a sample kit with instructions on how to login to the website so that you can consent to the study formally.</p>

<p>The level of analysis available to you will depend on your contribution but all participants will have to consent to be a part of the study.
The following tests are available:</p>
<ol>
<li>Find out who is in your microbiome - which bacteria and other microbes that are similar to bacteria called archaea are present in your child's sample ($99/swab kit);</li>
<li>You plus the world - This is two kits: 1 for your child and one for someone from Africa, South America or Asia. Your support of for the second sample will allow us to sequence more people from around the world as part of our ongoing research ($129/kit);</li>
<li>Microbes for two, three or four - which bacteria and other microbes that are similar to bacteria called archaea are present in your child's sample and one, two or three other samples;</li>
<li>A week of feces - seven stool swab samples to be used any way you want - to track the effects of an antibiotic on your gut, effect of foreign travel e.g. ($500/7sample kit);</li>
<li>All in the Family - Where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shallow shotgun metagenomic analysis") of up to four fecal samples with analysis of the pathways used by bacteria to signal other bacteria or within themselves;</li>
<li>Beyond Bacteria - Deeper shotgun metagenome and virome characterization (where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present making use of additional gene parts that can tell us if there are any associated viruses or virus products that "talk " with bacteria, fungus and parasites that may be present in the sample from your gut.  Requires shipment of a whole stool sample (materials and return FedEx postage included) ($2500/kit);</li>
<li>Functional Feces - Additional characterization of gut samples over time (up to 7 stool samples, providing an analysis of the variability of functions over time. Here too the DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shotgun metagenomic analysis").</li>
</ol>
<p>We will analyze all samples where the consent form and questionnaire is completed.  The samples in the project (including your child's) will be analyzed and published as a scientific article defining the range of diversity in the human microbiome.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed list of the different organisms present in your sample (taxonomy summary).</p>
<p>We would like you to understand from the consent what we will do with your child's sample and what you will get in return.</p>

<p>We will ask you to complete an online questionnaire about your child's lifestyle and what he/she eats.  We estimate that this should take no more than 30 minutes. You will then sample a part of your child's body (of interest to you) with a sterile Q-tip like swab by rubbing the surface of your skin, rubbing the surface of your tongue or sampling your stool by inserting the tip of the swab into used toilet tissue.  You can also sample other parts of her/his body - ear, nose, vagina, scalp, sole of foot. The swabs should be returned to us in the envelope provided using regular US mail service. DNA will be extracted from the sample and amplified by PCR (polymerase chain reaction) and then sequenced to see what bacteria are present and in what proportion in your sample. We estimate that it will take 2 months for you to learn the results.</p>
<p>For the Beyond Bacteria package you will submit a whole stool sample in a designated collection device on special ice packs (that reliably cool the sample to -20 degrees celsius/-4 degrees Fahrenheit) packed in a container that we will provide. The results for "Beyond Bacteria" and "All in the family" will take longer because more extensive analysis is provided.  Results will be uploaded to your American Gut account when they are available.  We are also asking you to consent to having your child's sample or the bacterial DNA from it to be used in future studies.</p>

<p style='font-weight: bold;'>Please Note: The sequencing is not for diagnostic purposes.</p>

<p style='font-weight: bold;'>How much time will each study procedure take, what is your child's total time commitment, and how long will the study last?</p>
<p>To complete the online questionnaire should take 30 minutes or less.  Each sample you send can be obtained in 5 minutes or less.  We expect the study to continue for 5 years but the results will be available to you before the end of the study (usually within 2 months of us receiving the sample).  You can choose to sample your child more than once.  If your child's personal details change (e.g. address, or heath status) we request that you voluntarily re-enter that information into the questionnaire.</p>

<p style='font-weight: bold;'>What risks are associated with this study?</p>
<p>The sampling techniques have been used for ~5 years with no reported side effects. We do not target the human DNA that may be in the sample so personal information about your child's genome will not be available.  The investigation personnel have taken precautions to ensure that there is minimal risk of loss of confidentiality.  Should confidentiality be compromised, the implications to your child are minimal since the results are not diagnostic and have no implications for insurance companies that could compromise your child's insurability.</p>
<p>Because this is a research study, there may be some unknown risks that are currently unforeseeable. You will be informed of any significant new findings.</p>

<p style='font-weight: bold;'>What are the alternatives to participating in this study?</p>
<p>The study is entirely voluntary and not allowing your child to participate will have no consequence.  There is no alternative test.</p>

<p style='font-weight: bold;'>What benefits can be reasonably expected?</p>
<p>There is no direct benefit to your child for participating in this study. The investigator, however, may learn more about the human microbiome in health and disease and provide a valuable resource for other researchers in other studies.</p>

<p style='font-weight: bold;'>Can you choose to not to have your child participate or withdraw from the study without penalty or loss of benefits?</p>
<p>There is no direct benefit to you or your child for participating in this study. We believe that there may be natural curiosity to know what bacteria are in your sample and how this compares to other people of the same gender and age. The investigator, however, will learn more about the human microbiome in health and disease and provide a valuable resource for other researchers in other studies.  Your contribution to the project may be eligible as a tax-deduction.  The receipt will be sent to you from the site that handles financial contributions.</p>

<p style='font-weight: bold;'>We will analyze all samples where the consent form and questionnaire is completed.  The samples in the project (including your child's) will be analyzed and published as a scientific article.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed taxa report of your results.</p>
<p>The results from analysis of your sample/s cannot be used by you or your doctor to confirm a clinical diagnosis and we are not testing for infectious disease.</p>

<p style='font-weight: bold;'>Can your child be withdrawn from the study without your consent?</p>
<p>Participation in research is entirely voluntary. You may refuse to participate or withdraw your child from the study at any time, without penalty or loss of benefits to which you are entitled. If you decide that you no longer wish to continue in this study, you will be requested to contact the American Gut Project helpline to inform us of your intent to withdraw.  If your sample has not been processed you may request a refund which will be processed through the site where you contributed to the project.</p>
<p>You will be told if any important new information is found during the course of this study that may affect your wanting to continue.</p>

<p style='font-weight: bold;'>Will you be compensated for participating in this study?</p>
<p>You will not be financially compensated in this study.</p>

<p style='font-weight: bold;'>Are there any costs associated with participating in this study?</p>
<p>You will be asked to contribute money to the project commensurate with the investigation you request ($99 for one sample, $1500 for "All in the family" (shallow shotgun metagenomic sequencing) and $2500 for "Beyond Bacteria" (deeper shotgun metagenome and virome characterization of one sample, plus additional sequencing). A receipt will be sent to you after you pay for the analysis you are requesting.  These contributions are used to partially finance the project.  Any additional funds required are provided from the funds UCSD has provided to Dr. Knight to set up his laboratory.</p>

<p style='font-weight: bold;'>What if your child is injured as a direct result of being in this study?</p>
<p>If your child is injured as a direct result of participation in this research, the University of California will provide any medical care you need to treat those injuries. The University will not provide any other form of compensation to you if your child is injured. You or your child may call the Human Research Protections Program Office at (858) 246-7444 for more information about this, to inquire about your rights as a research subject or to report research-related problems.</p>

<p style='font-weight: bold;'>What about your confidentiality?</p>
<p>Research records will be kept confidential to the extent allowed by law. All data about your child that is entered on the web site is stored on a password-protected server located at the SDSC (San Diego Supercomputer Center) card access controlled facility at UCSD.  Financial information from participants contributing to the project is not accessible to the researchers.  The code key (that relates participant personal information to sample barcodes) is retained on a separate password-protected server that is accessible only to the PI, Co-I, sample coordinator and the database coders.  All analysis is done on de-identified data and the data deposited in a public repository for use by other investigators, is similarly de-identified. Research records may be reviewed by the UCSD Institutional Review Board.</p>
<p>You will provide information about yourself that could allow you to be identified if it was made public e.g. name, age, birthdate, address.  We have made every effort to ensure that you cannot be identified from the data you supply about yourself but retaining critical information like gender, age without compromising your personal information or the data integrity.</p>
<p>We may need to report information about known or reasonably suspected incidents of abuse or neglect of a child, dependent adult or elder including physical, sexual, emotional, and financial abuse or neglect. The only way we could discover such abuse is if it is self-reported by the participant or the legal guardian, so this is not likely.  If any investigator has or is given such information, he or she may report such information to the appropriate authorities.</p>

<p style='font-weight: bold;'>Who can you call if you have questions?</p>
<p>If you have questions or research-related problems, you may reach Rob Knight at 858-246-1184 or contact Brent Erickson at 858-534-8739.</p>

<p>You may call the Human Research Protections Program Office at (858) 246-7444 to inquire about your rights as a research subject or to report research-related problems.</p>

<p style='font-weight: bold;'>Your Signature and Consent</p>
<p>You have received a copy of this consent document and a copy of the "Experimental Subject's Bill of Rights" to keep.</p>

<p>You agree to allow your child to participate.</p>''',
    'PARTICIPATION_AGREEMENT': '''<p style="text-align: center;font-weight: bold;">AMERICAN GUT PROJECT</p>
<p style="text-align: center;font-weight: bold;">University of California, San Diego</p>
<p style="text-align: center;font-weight: bold;">PARTICIPATION AGREEMENT</p></b>
<ol><li><b>Indemnification.</b> Each party shall defend, indemnify and hold the other party, its officers, employees, and agents harmless from and against any and all liability, loss, expense (including attorneys' fees), and claims for injury or damages arising out of the performance of this Agreement, but only in proportion to and to the extent such liability, loss, expense, attorneys' fees, or claims for injury (including death) or damages are caused by or result from the negligent or intentional acts or omissions of the indemnifying party, its officers, employees, or agents.</li>
<li><b>Patent Infringement Indemnification.</b>  The Individual shall indemnify, defend, and hold harmless UCSD, its officers, agents, and employees against all losses, damages, liabilities, costs, and expenses (including but not limited to attorneys' fees) resulting from any judgment or proceeding in which it is determined, or any settlement agreement arising out of the allegation, that the Individual's furnishing or supplying UCSD with parts, goods, components, programs, practices, or methods under this Agreement or UCSD's use of such parts, materials, goods, components, programs, practices, or methods supplied by the Individual under this Agreement constitutes an infringement of any patent, copyright, trademark, trade name, trade secret, or other proprietary or contractual right of any third party. UCSD retains the right to participate in the defense against any such suit or action.</li>
<li><b>Limitation of Liability.</b>  EXCEPT WITH REGARD TO ITS INDEMNIFICATION OBLIGATIONS, NEITHER PARTY WILL BE LIABLE TO THE OTHER PARTY FOR ANY INDIRECT, SPECIAL, INCIDENTAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES, OR COSTS, INCLUDING, BUT NOT LIMITED TO, ANY LOST PROFITS OR REVENUES, EVEN IF SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES AND REGARDLESS OF THE LEGAL THEORY UNDER WHICH SUCH DAMAGES ARE SOUGHT.  UCSD DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL UCSD'S TOTAL LIABILITY UNDER THIS AGREEMENT EXCEED THE AMOUNT PAID BY THE INDIVIDUAL FOR THE SERVICES. UCSD DOES NOT GUARANTEE A SPECIFIC RESULT OR DELIVERABLE FOR PARTICIPATING IN THIS PROJECT.</li>
<li><b>UCSD's Ownership of Materials.</b>  UCSD will own the deliverables upon receipt of the materials from Individual.</li>
<li><b>Use of UCSD Name.</b>  California Education Code Section 92000 prohibits use of the University of California, San Diego's name to suggest that UCSD endorses a product or service. The Individual will not use The University of California's name, or any acronym thereof publically, including UCSD, without UCSD's prior written approval.</li>
<li><b>Excusable Delay.</b>  In the event of a delay caused by inclement weather, fire, flood, strike or other labor dispute, acts of God, acts of Governmental officials or agencies, or any other cause beyond the control of UCSD, UCSD's performance is excused hereunder for the periods of time attributable to such a delay, which may extend beyond the time lost due to one or more of the causes mentioned above. The Company's duty to pay for past or continuing costs is not suspended hereunder.</li>
<li><b>Non-Interference.</b> Notwithstanding any other provision contained herein, the use of UCSD facilities and/or UCSD personnel in support of this Agreement can only be authorized to the extent that it will not interfere with work related to the prime missions of UCSD and/or the Department (e.g., education and research).  Accordingly, Individual's exclusive remedy for failure by either UCSD or persons acting on its behalf to perform services or furnish information or data hereunder at any particular time or in any specific manner, is limited to reimbursement of any unexpended payments under this Agreement.</li>
<li><b>Non-Exclusive Nature of Services.</b>  The Services herein are being offered to Individual on a non-exclusive basis.  Nothing herein shall be construed as granting Company any exclusive right(s) to the Service(s) referenced herein, and UCSD retains the right to offer and perform similar or identical Services for others.</li>
<li><b>Notice.</b>  Any notice or communication required by this Agreement shall be in writing and shall be deemed to have been duly given if delivered personally, or sent by overnight mail, or prepaid registered mail, email, or confirmed facsimile transmission, addressed to the other party at the address set forth on kit registration, or at such other address as such party hereto may hereafter specify in writing to the other party.</li>
<li><b>Status of Parties.</b>  This Agreement is not intended to create, nor shall it be construed to be, a joint venture, association, partnership, franchise, or other form of business relationship.  Neither party shall have, nor hold itself out as having, any right, power or authority to assume, create, or incur any expenses, liability, or obligation on behalf of the other party, except as expressly provided herein.</li>
<li><b>Third-Party Beneficiary.</b>  There are no intended third-party beneficiaries to this Agreement.</li>
<li><b>Severability.</b>  If any provision of this Agreement is held invalid, illegal or unenforceable in any respect, such provision shall be treated as severable, leaving the remaining provisions unimpaired, provided that such does not materially prejudice either party in their respective rights and obligations contained in the valid terms, covenants, or conditions.</li>
<li><b>Non-Waiver.</b>  The failure of either party to require the performance of any of the terms of this Agreement or the waiver by either party of any default under this Agreement shall not prevent a subsequent enforcement of such term, nor be deemed a waiver of any subsequent breach.</li>
<li><b>Modification of Agreement.</b>  This Agreement shall be changed only by written agreement of the parties.</li>
<li><b>Applicable Law.</b>  This Agreement shall be governed by the laws of the State of California without regard to its conflict of laws provisions.</li>
<li><b>Signatures, Counterparts and Copies.</b>  This Agreement may be executed in counterparts, all of which, when taken together, shall constitute one contract with the same force and effect as if all signatures had been entered on one document.  Signatures may be made electronically, by clicking "I Agree" and such electronic signatures shall be valid and binding upon the parties making them, and shall serve in all respects as original signatures. Upon clicking "I Agree" this agreement shall be considered fully-executed by both parties. Signatures may be delivered among and between the parties by facsimile or electronic means.  Thereafter, the parties further agree that electronic copies of this Agreement may be used for any and all purposes for which the original may have been used.</li>
<li><b>Arbitration.</b>  In the event of any dispute, claim, question, or disagreement arising from or relating to this Agreement or the breach thereof, the parties hereto shall use their best efforts to settle the dispute, claim, question, or disagreement.  To this effect, they shall consult and negotiate with each other in good faith and recognizing their mutual interests, attempt to reach a just and equitable solution satisfactory to both parties.  If they do not reach a solution within a period of sixty (60) days, then upon notice by either party to the other, all disputes, claims, questions, or disagreements shall be finally settled in accordance with the provisions of the American Arbitration Association ("AAA") and proceed under the provisions of Title 9 of the California Code of Civil Procedure Sections 1280 through and including 1294.2.  The discovery provisions of the California Code of Civil Procedure Section 1283.05 shall be applicable to this Agreement.  Each party shall bear its own costs.</li>
<li><b>Export Control.</b>  No ITAR or export controlled materials shall be delivered to UCSD pursuant to this agreement.   </li>
<li><b>Entire Agreement.</b>  This Agreement, including Exhibit A made a part hereof, sets forth the entire agreement of the parties with respect to the subject matter herein and supersedes any prior agreements, oral and written, and all other communications between the parties with respect to such subject matter.</li>
</ol><br/>''',
    'EXHIBIT_A': '''<p style="text-align: center;font-weight: bold;">EXHIBIT A</p>
<p style="text-align: center;font-weight: bold;">AMERICAN GUT PROJECT STATEMENT OF SERVICES</p>
<ol>
<li><b>SCOPE OF WORK:</b>
<p>The Services will be performed as set forth below or in accordance with the attachment hereto and incorporated by reference herein.</p>
<p>When you sign up for the study, you may claim a package of research analyses based on your contribution level.  You are mailed a kit with sampling instructions, and directions on how to sign into the website to complete the consent form and submit the questionnaire.  Any sample that is received in the laboratory without a completed consent form online is not sequenced.  You be able to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed taxa report of your results - which can be viewed online and downloaded into Excel.</p>
<p>I have accepted this Scope of Work on behalf of UCSD and the responsibility for administering and monitoring the agreement.</p>
</li>
<li><b>DELIVERABLES:</b>
<p>Approximately 8-10 weeks after we have received your sample you will be notified of your results electronically.</p>
</li>
<li><b>COST:</b>  Cost is variable based on the contribution level that was elected.
</li>
<li><b>PAYMENT</b></li>
<ol><li><b>SCHEDULE:</b> 100% of cost due upon clicking "I Accept"</li>
<li><b>REMITTANCE:</b>  Payment will be submitted through PayPal via the FundRazr website.</li>
</ol>
<li><b>TERM OF AGREEMENT:</b> This Agreement will be effective as of the date of remittance of payment to FundRazr.</li>
<li><b>UCSD CONTRACT OFFICER CONTACT:</b><br/>
Karim Hussein<br/>
University of California, San Diego<br/>
9500 Gilman Drive Mail Stop 0934<br/>
La Jolla, California 92093-0934<br/>
Telephone: (858) 822-5180<br/>
Email: khussein@ucsd.edu''',
    'BILL_OF_RIGHTS': '''Experimental Subject's Bill of Rights''',
    'TEXT_I_HAVE_READ_1': 'I have read (or someone has read to me) this form. I am aware that I am being asked to be in a research study. I voluntarily agree to be in this study.',
    'TEXT_I_HAVE_READ_SIMPLIFIED': 'Yes, you will be in this research study.',
    'PERSON_ATTAINING_ASSENT': 'Signature Of Person Obtaining Assent',
    'TEXT_ASSENT_WITNESS': 'In my judgment, the participant is voluntarily and knowingly giving assent and possesses the legal capacity to give assent to participate in the study.',
    'OBTAINER_NAME': 'Name of person obtaining assent',
    'TEXT_I_HAVE_READ_PARENT': 'I have read (or someone has read to me) this form. I am aware that my child is being asked to be in a research study. I voluntarily agree for my child to be in this study.',
    'PARTICIPANT_NAME': 'Participant name',
    'PARTICIPANT_EMAIL': 'Participant email',
    'PARTICIPANT_PARENT_1': 'Parent/Guardian name',
    'PARTICIPANT_PARENT_2': 'Parent/Guardian name of second parent',
    'PARTICIPANT_DECEASED_PARENTS': 'One parent/guardian is deceased or unable to consent.',
    'DATE_SIGNED': 'Date Signed',
    'PARTICIPANT_ADDRESS': 'Participant Address',
    'PARTICIPANT_CITY': 'Participant City',
    'PARTICIPANT_STATE': 'Participant State',
    'PARTICIPANT_ZIPCODE': 'Participant Zipcode',
    'PARTICIPANT_COUNTRY': 'Participant Country'
}

_MAP = {
    'MAP_TITLE': 'Map Key',
    'MAP_PARTICIPANT': ' Participant',
    'MAP_KIT': ' Kit Verified',
    'MAP_SAMPLE': ' Sample(s) Logged',
    'SEP1': '1-10 kits',
    'SEP2': '11-100 kits',
    'SEP3': '101-1000 kits',
    'SEP4': '1001-10000 kits',
    'SEP5': '>10000 kits'
}

_FORGOT_PASSWORD = {'ENTER_ID_EMAIL': 'Enter your Kit ID and email',
                    'KIT_ID': 'Kit ID:',
                    'EMAIL': 'E-mail',
                    'EMAIL_RESET_PASSWORD': 'You will receive an email shortly with instructions to reset your password. Please check your email because you need to reset your password within two hours.',
                    'EMAIL_FAILED': '<p>There was a problem sending you the password reset code. Please contact us directly at <a href=\"mailto:%(help_email)s\" target=\"_blank\">%(help_email)s</a>.</p><p>Email contained: </p>' % {'help_email': media_locale['HELP_EMAIL']},
                    'NO_RECORD': '<p style="color:red;">This information does not match our records</p><p>Please email <a href="mailto:%(help_email)s">directly</a> for further assistance<p>' % {'help_email': media_locale['HELP_EMAIL']},
                    'SEND_EMAIL': 'Send email'}

_ERROR = {
    'ERROR_OCCURED': 'AN ERROR HAS OCCURED!',
    'ERROR_CONTACT': "The error has been logged and we will look into it. Please go back to the main page."
    }

_RETREIVE_KITID = {
    'UNKNOWN_EMAIL': 'This email address is not in our system',
    'ENTER_EMAIL': 'Please Enter Your Email',
    'SEND_EMAIL': 'Send Kit ID Email',
    'EMAIL_SUCCESS': 'Your kit ID has been emailed to you. Please check your email.',
    'EMAIL_CANTSEND': 'Mail can be sent only from microbio.me domain.',
    'EMAIL_EXCEPTION': 'There was a problem sending you the kit ID. Please contact us directly at <a href=\"mailto:%(help_email)s\">%(help_email)s</a>.' % {'help_email': media_locale['HELP_EMAIL']},
    'EMAIL_PROMPT': 'Email:'
    }

_ADD_SAMPLE = {
    'NEW_SAMPLE_TITLE': 'Log a new sample for',
    'NEW_SAMPLE_DESCRIPTION_1': 'Choose the barcode from your kit that corresponds to the sample you are logging.',
    'NEW_SAMPLE_DESCRIPTION_2': 'It is very important that the sample barcode matches <strong>exactly</strong> for downstream analysis steps.',
    'SITE_SAMPLED': 'Site Sampled',
    'DATE': 'Date',
    'DATE_EXAMPLE': ' mm/dd/yyyy (Example: 05/07/2013)',
    'TIME': 'Time',
    'TIME_EXAMPLE': ' hh:mm AM/PM (Example: 04:35 PM)',
    'NOTES': 'Additional Notes (optional)',
}

_REGISTER_USER = {
    'ENTER_KIT_ID': "Please enter your kit ID",
    'ENTER_PASSWORD': 'Please enter your kit password',
    'ENTER_NAME': 'Please enter your name',
    'ENTER_EMAIL': 'Please enter your email',
    'MATCHING_EMAIL': 'Emails do not match',
    'REQUIRED_EMAIL': 'You must supply a valid email',
    'ENTER_ADDRESS': 'Please enter your address',
    'ENTER_CITY': 'Please enter your city',
    'ENTER_STATE': 'Please enter your state',
    'ENTER_ZIP': 'Please enter your zip',
    'ENTER_COUNTRY': 'Please enter your country',
    'REQUIRED_ZIP': 'Your zip must be 10 or fewer characters',
    'EMAIL': 'Email',
    'EMAIL2': 'Re-enter email',
    'NAME': 'Name',
    'ADDRESS': 'Address',
    'CITY': 'City',
    'STATE': 'State',
    'ZIP': 'Zip',
    'COUNTRY': 'Country',
    'PASSWORD': 'Password',
    'KIT_ID': 'Kit ID',
    'SUBMIT': 'Submit My Information'
}

_ADDENDUM = {
    'TITLE': 'American Gut Addendum',
    'INTRO': 'We\'d like to note that in general these data allow you to understand how similar or different you are to other people in terms of the bacterial composition of the sample you sent. The information about the microbes is at as fine level of a taxonomic resolution as we were able to achieve with our sequencing methods, and varies for different groups of microbes. Currently, we cannot tell you what it means if you have more or less of a certain bacteria than other people. Gut microbiome research is still new, and we have a lot to learn. Your participation in the American Gut Project will allow us to learn more, and we hope to update you with new findings as they emerge.',
    'LEARN_MORE': 'Learn more about your certificate by clicking on a plot or table',
    'MOD01ALT': 'Your American Gut Sample',
    'MOD01bALT': 'Michael Pollan',
    'MOD02ALT': 'What\'s in your sample?',
    'MOD11ALT': 'Taxonomy Bar Charts',
    'MOD12ALT': 'Major Phyla',
    'MOD13ALT': 'Abundant Microbes',
    'MOD14ALT': 'Enriched Microbes',
    'MOD15ALT': 'Rare Microbes',
    'MOD03ALT': 'How do your gut microbes compare to others?',
    'MOD08ALT': 'PCoA of BodySites with HMP',
    'MOD09ALT': 'PCoA of diets and age',
    'MOD10ALT': 'PCoA of American Gut Data',
    'RESULTS_CAPTION': 'Your certificate is designed to help you determine what was found in your sample, and how you compare to other people. Click on a graph or table to learn more.',
    'SAMPLE_TITLE': 'What\'s in your %(PROJECT_TITLE)s sample?' % media_locale,
    'TAXONOMY': 'Taxonomy',
    'TAXONOMY_INTRO': 'Taxonomy is a system scientists use to describe all life on the planet. Taxonomy is commonly referred to as an organism\'s scientific name. This name allows us to understand how closely related two organisms are to each other. There are seven major levels of taxonomy that go from less specific to more specific. The phylum level represents very broad range of organisms that have <strong>evolved over hundreds of millions of years</strong> whereas the species level represents only a small subset of them that are <strong>much more closely related</strong>. Typically, names at the genus and species levels are written in <em>italics</em> or are <u>underlined</u> (in our tables, they are <em>italicized</em>). For instance, here is the list of taxonomic levels and names for humans and chimpanzees:',
    'HUMAN_TAXONOMY': 'Human',
    'HUMAN_TAXONOMY_KINGDOM': 'Kingdom: Animalia',
    'HUMAN_TAXONOMY_PHYLUM': 'Phylum: Chordata',
    'HUMAN_TAXONOMY_CLASS': 'Class: Mammalia',
    'HUMAN_TAXONOMY_ORDER': 'Order: Primates',
    'HUMAN_TAXONOMY_FAMILY': 'Family: Hominidae',
    'HUMAN_TAXONOMY_GENUS': 'Genus: <em>Homo</em>',
    'HUMAN_TAXONOMY_SPECIES': 'Species: <em>sapiens</em>',
    'CHIMP_TAXONOMY': 'Chimpanzee',
    'CHIMP_TAXONOMY_KINGDOM': 'Kingdom: Animalia',
    'CHIMP_TAXONOMY_PHYLUM': 'Phylum: Chordata',
    'CHIMP_TAXONOMY_CLASS': 'Class: Mammalia',
    'CHIMP_TAXONOMY_ORDER': 'Order: Primates',
    'CHIMP_TAXONOMY_FAMILY': 'Family: Hominidae',
    'CHIMP_TAXONOMY_GENUS': 'Genus: <em>Pan</em>',
    'CHIMP_TAXONOMY_SPECIES': 'Species: <em>troglodytes</em>',
    'LACTO_TAXONOMY': 'Here is the same list for a common yogurt bacterium (<em>Lactobacillus delbrueckii</em>):',
    'LACTO_TAXONOMY_KINGDOM': 'Bacteria',
    'LACTO_TAXONOMY_PHYLUM': 'Firmicutes',
    'LACTO_TAXONOMY_CLASS': 'Bacilli',
    'LACTO_TAXONOMY_ORDER': 'Lactobacillales',
    'LACTO_TAXONOMY_FAMILY': 'Lactobacillaceae',
    'LACTO_TAXONOMY_GENUS': '<em>Lactobacillus</em>',
    'LACTO_TAXONOMY_SPECIES': '<em>delbrueckii</em>',
    'BACTAX_LINK': 'For more information on bacterial taxonomy, please refer to the following link: ',
    'TOP': 'Back to the top',
    'TAX_BARCHART': 'Taxonomy Bar Chart',
    'TAX_BARCHART_TEXT_1': 'The taxonomy bar chart shows the abundances of bacterial types at the phylum level in your sample and compares it to other samples. Specifically, it shows you what percentage of all your bacteria belonged to each phyla. We also calculated the average percentage of each bacterial phylum across all samples, across samples from people with a similar diet to the one you reported, across samples from people of the same gender as you, across samples from everyone with a similar BMI to you, across samples from everyone with the same age as you, and for one specific person, Michael Pollan. You can compare the percentage of bacterial phyla in your sample (first bar) to all of these values to get an idea of how similar or different you are.',
    'TAX_BARCHART_TEXT_2': '<strong>Firmicutes and Bacteroidetes are the two most abundant bacterial phyla in the human gut, but others are also present.</strong> Please see <a href = "#phyla">Major Bacterial Phyla</a> below for basic descriptions of these phyla.',
    'ABUNDANT': 'Abundant Microbes',
    'YOUR_ABUNDANT': 'Your most abundant microbes:',
    'YOUR_ABUNDANT_TABLE_HEADER': '<th>Taxonomy</th><th>Sample</th>',
    'OBSERVED_TAXON_1': '<td class = \'taxa\'>Family Prevotella</td><td class = \'row\'>24.9%</td>',
    'OBSERVED_TAXON_2': '<td class = \'taxa\'>Family Ruminococcaceae</td><td class = \'row\'>13.4%</td>',
    'OBSERVED_TAXON_3': '<td class = \'taxa\'>Family Lachnospiraceae</td><td class = \'row\'>10.1%</td>',
    'OBSERVED_TAXON_4': '<td class = \'taxa\'>Genus <em>Bacteroides</em></td><td class = \'row\'>8.1%</td>',
    'TAX_BARCHART_EXP': 'The first table shows the four most abundant groups of microbes in your sample. Although you had other bacteria, these are the ones that you have the most of. The percentages on the right (under &quot;Sample&quot;) tell you what percent of all of your bacteria belong to these taxa.',
    'ENRICHED': 'Enriched Microbes',
    'YOUR_ENRICHED': 'Your most enriched microbes:',
    'YOUR_ENRICHED_TABLE_HEADER': '<th>Taxonomy</th><th>Sample</th><th>Population</th><th>Fold</th>',
    'YOUR_ENRICHED_1': '<td class = \'taxa\'>Genus <em>Clostridium</em></td><td class = \'row\'>2.5%</td><td class = \'row\'>0.3%</td><td class = \'row\'>7x</td>',
    'YOUR_ENRICHED_2': '<td class = \'taxa\'>Genus <em>Finegoldia</em></td><td class = \'row\'>0.7%</td><td class = \'row\'>0.0%</td><td class = \'row\'>17x</td>',
    'YOUR_ENRICHED_3': '<td class = \'taxa\'>Genus <em>Prevotella</em></td><td class = \'row\'>24.9%</td><td class = \'row\'>2.6%</td><td class = \'row\'>9x</td>',
    'YOUR_ENRICHED_4': '<td class = \'taxa\'>Genus <em>Collinsella</em></td><td class = \'row\'>0.9%</td><td class = \'row\'>0.1%</td><td class = \'row\'>8x</td>',
    'ENRICHED_EXP_1': 'The second table shows four microbes that you had more of compared to other people. It is likely that other participants also have these microbes in their sample, but we found substantially higher abundances of them in your sample relative to others. The percentages on the right tell you how many of your total bacteria (under &quot;Sample&quot;) or of the total bacteria in an average person&amp;s sample (under &quot;Population&quot;) belong to these taxa. Since you have more of these bacteria than most other people, the percentage under &quot;Sample&quot; should be higher than the percentage under &quot;Population&quot;.',
    'ENRICHED_EXP_2': 'The fold change tells you how many more of these bacteria you have than the average participant. For example, if you have 20% Bacteria A and the average person in the population has 10% Bacteria A, you have twice as many Bacteria A. This would be a twofold (2x) difference. Please note that because the percentages we report on this sheet are rounded (e.g., 0.05% rounded to 0.1%), and your fold differences are calculated from values that are not rounded, the fold differences you see may be slightly distinct than what you would calculate based on the numbers you see.',
    'RARE': 'Rare Taxa',
    'RARE_TEXT_1': 'This sample included the following rare taxa: Genus <em>Varibaculum</em>, Genus <em>Neisseria</em>, Genus <em>Campylobacter</em>, Unclassified Order ML615J-28.',
    'RARE_TEXT_2': 'This line shows four microbes that you have that are not commonly found in the type of sample you provided. Some other people may have them, but most people do not.',
    'YOUR_COMPARE': 'How do your gut microbes compare to others?',
    'COMPARE_TEXT_1': 'Here, we present three Principle Coordinates Plots. Each point on these plots represents the bacterial composition of one sample from one person. We take all of the information about the abundances of all the bacteria in each sample and compare them to each other using this type of plot. When two points are very close to each other, it means that the types of bacteria in those two samples are very similar. Points that are farther apart represent samples that are less similar to each other. The axes mean nothing in this context. It doesn\'t matter how high or low a point is on the plot. The only thing that matters is how close it is to other points.',
    'COMPARE_TEXT_2': 'The large point represents your sample on each plot. This allows you to see how similar (close to) or different (far from) your sample is from others.',
    'DIFFERENT_BODY_SITES': 'DIfferent Body Sites',
    'DIFFERENT_BODY_SITES_ALT': 'PCoA by body site for AGP and HMP',
    'DIFFERENT_BODY_SITES_TEXT': 'This plot lets you compare your sample to samples collected in other microbiome projects from several body sites. The color of each point tells you which project and body site the sample came from. HMP refers to the <a href = \'http://www.hmpdacc.org\'>Human Microbiome Project</a>, funded by the National Institutes of Health. You can see how your sample compared to fecal, oral, and skin samples from the Human Microbiome Project, as well as to fecal, oral, and skin samples from the American Gut Project, the Global Gut Project, and the Personal Genome Project. These samples have been combined in any category not labeled &quot;HMP&quot;. The oval around each group of points shows you where an average sample from each project and body site should fall on the plot. These sometimes make it easier to see the patterns all the clusters of points make.',
    'DIFFERENT_AGES_POPS': 'Different Ages and Populations',
    'DIFFERENT_AGES_POPS_ALT': 'PCoA of international populations colored by age',
    'DIFFERENT_AGES_POPS_TEXT': 'This plot lets you compare your sample to other fecal microbiome samples according to age and place of origin. The color of each point indicates the age of the person the sample was collected from, with red being the youngest and purple being the oldest. Also, on this plot, the ovals show where in the world each sample came from. The red oval shows you the area where an average sample from a Western country should fall. The yellow oval shows you where an average sample from an Amerindian population in Venezuela should fall. The blue oval shows you where an average sample from Malawi should fall. These data are from <a href = \'http://www.nature.com/nature/journal/v486/n7402/abs/nature11053.html\'>Yatsunenko et al. 2012</a>. We used these populations as a comparison to your sample since a large number of people with diverse ages were sampled in these populations. We have fewer data from other populations in other parts of the world.',
    'AG_POPULATION': 'The American Gut Population',
    'AG_POPULATION_ALT': 'PCoA of American Gut population colored by Firmicutes',
    'AG_POPULATION_TEXT': 'This plot lets you compare your sample to other fecal microbiome samples we collected from American Gut participants. The color indicates the relative abundance of Firmicutes bacteria each sample had with red being the lowest and purple being the highest. If you had a lot of Firmicutes bacteria, then your sample should be purple, and you can look for other purple samples to see how similar your whole bacterial community is to other people with high amounts of Firmicutes. As in the other plots, the location of the point along the axes means nothing. Only its relative position compared to the other points is meaningful.',
    'MAJOR_PHYLA': 'Major Bacterial Phyla',
    'MAJOR_PHYLA_FIRMICUTES_HEADER': 'Firmicutes',
    'MAJOR_PHYLA_FIRMICUTES_TEXT': 'A phylum of bacteria with generally Gram-positive (retain crystal violet dye) staining cell wall structure. The names is derived from Latin <em>firmus</em> for strong and <em>cutis</em> for skin. The cells are in the form of spheres called cocci (singular coccus) or rods called bacilli (singular bacillus). Firmicutes encompass bacteria that can be found in many different environments ranging from soil to wine to your gut. There are currently more than 274 genera representing 7 different classes of which Clostridia (anaerobes - no oxygen) and Bacilli (obligate or facultative aerobes) are the most significant. Both classes are predominantly saprophytic (getting nourishment from dead or decaying organic matter) playing an important role in the decomposition and nutrient mineralization processes, but also contain a few human pathogens (e.g. <em>Clostridium tetani</em> or <em>Bacillus anthracis</em>).',
    'MAJOR_PHYLA_BACTEROIDETES_HEADER': 'Bacteroidetes',
    'MAJOR_PHYLA_BACTEROIDETES_TEXT': 'A phylum of Gram-negative bacteria, rod-shaped, present in all sorts of environments such as soil, sediments, and fresh and marine waters. Most are saprophytic and involved in carbon cycling. Often abundant in nutrient-rich habitats and so they are a major component of animal guts where they can act as degraders of complex carbohydrates and proteins but also as pathogens. Their representatives are organized within 4 major classes among which the genus <em>Bacteroides</em> in the class of Bacteroidia is the most prevalent and the most studied. Bacteroidetes together with Firmicutes make up the majority of gut bacteria. The ratio of these two types of bacteria (specifically the dominance of Firmicutes over Bacteroidetes) may be linked to obesity.',
    'MAJOR_PHYLA_PROTEOBACTERIA_HEADER': 'Proteobacteria',
    'MAJOR_PHYLA_PROTEOBACTERIA_TEXT': 'A phylum of Gram-negative bacteria. They are named after a Greek God Proteus to illustrate their variety of forms. They are organized in 6 recognized classes and represent all types of metabolisms ranging from heterotrophic to photosynthetic to chemoautotrophic.  They include many well-known pathogens (e.g., <em>Escherichia</em>, <em>Helicobacter</em>, <em>Salmonella</em>, <em>Vibrio</em>) as well as free-living types that can fix nitrogen (convert nitrogen present in the atmosphere into ammonia, a form of nitrogen available for plants\' uptake).',
    'MAJOR_PHYLA_ACTINOBACTERIA_HEADER': 'Actinobacteria',
    'MAJOR_PHYLA_ACTINOBACTERIA_TEXT': 'A phylum of Gram-positive bacteria both terrestrial and aquatic. They are mostly recognized as excellent decomposers of resilient organic compounds such as cellulose or chitin. Although some can be plant and animal pathogens, others are more known as producers of antibiotics (e.g. Streptomyces).  In their body form, many resemble fungi by forming mycelial-like filaments.',
    'MAJOR_PHYLA_VERRUCOMICROBIA_HEADER': 'Verrucomicrobia',
    'MAJOR_PHYLA_VERRUCOMICROBIA_TEXT': 'A relatively new phylum with only a handful of described species. Although not the most abundant, they seem to be always present in soil, aquatic environments, and feces. Most likely they are involved in the decomposition of organic matter, with no known pathogens. While some may be autotrophs, others can be internal symbionts of microscopic eukaryotes such as protists or nematodes. Their name is derived from a wart-like appearance (<em>verruca</em> means wart) but they do not cause warts.',
    'MAJOR_PHYLA_TENERICUTES_HEADER': 'Tenericutes',
    'MAJOR_PHYLA_TENERICUTES_TEXT': 'A phylum of Gram-negative bacteria without a cell wall (<em>tener</em> - soft, <em>cutis</em> - skin) which are organized in a single class. Nutritionally, they represent variable pathways ranging from aerobic and anaerobic fermenters to commensals to strict pathogens of vertebrates (e.g., fish, cattle, wildlife). Among the best studied are Mycoplasmas with a fried egg-like shape and <em>Mycoplasma pneumoniae</em> is one of the best known examples of human pathogens causing pneumonia, bronchitis, and other respiratory conditions.',
    'MAJOR_PHYLA_CYANOBACTERIA_HEADER': 'Cyanobacteria',
    'MAJOR_PHYLA_CYANOBACTERIA_TEXT': 'A phylum of photosynthetic (plant-like) bacteria. The name comes from their blue pigment (in Greek <em>kyanos</em> - blue). They can grow as single cells or form filamentous colonies. They are extremely successful in every imaginable environment including places where other organisms are extremely limited like hot springs or cold Antarctic bare rocks. Through their incredible diversity and abundance, they contribute significantly to the global cycle of oxygen.',
    'MAJOR_PHYLA_FUSOBACTERIA_HEADER': 'Fusobacteria',
    'MAJOR_PHYLA_FUSOBACTERIA_TEXT': 'A phylum of rod-shaped Gram-negative bacteria. Known primarily as fermentative species but some can be pathogens. Can occur in anoxic (no oxygen) sediments as well as intestinal habitats of animals including humans.',
    'CONTRIB': 'Contributors',
    'SUPPORTERS': 'Supporters',
    'SPONSORS': 'Sponsors',
    'COLLABORATORS': 'Collaborators'
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
    'VERIFICATION_TEXT_2': 'our <strong>Verification Code</strong> will be sent to you via email to the address that you entered when you made your contribution; if you made an anonymous contribution, please <a href="%(sitebase)s/authed/help_request/">contact us directly</a>.' % {'sitebase': media_locale['SITEBASE']},
    'VERIFICATION_TEXT_3': 'If you cannot find your <strong>Verification Code</strong>, please make sure to check your spam folder. If you still cannot find the code, please <a href="%(sitebase)s/authed/help_request/">contact us</a>.' % {'sitebase': media_locale['SITEBASE']},
    'RESEND_VERIFICATION': 'Resend verification code',
    'VERIFICATION_HEADER_2': 'Verify your identity and kit barcode(s)',
    'VERIFICATION_CODE_PROMPT': 'Please enter the verification code sent to your email address <a href="#" class="help" title="If you did not recieve a verification code in your email from American Gut, please check your spam folder. If you still cannot find it, contact %(help_email)s">(?)</a>' % {"help_email": media_locale["HELP_EMAIL"]},
    'VERIFICATION_CODE_ERROR': 'The kit verification code you entered does not match our records. Please double-check the code you entered. If you continue to experience difficulties, please <a href=/authed/help_request/>contact us</a>.',
    'VERIFY_BARCODES': 'Please verify that the barcode(s) you received in the mail match the barcode(s) here',
    'VERIFY_BARCODES_POPUP': 'The barcode you need to verify is located on the outside of your sample tube.',
    'SAMPLE_SOURCE_HEADER_1': 'Sample Source',
    'SAMPLE_SOURCE_TEXT_1': 'There are three different sample sources that you can choose from for the %(project)s. The sources are human, animal and environmental. The buttons below will allow you to add a new sample source.',
    'SAMPLE_SOURCE_TEXT_2': 'If you add a <strong>human</strong> or <strong>animal</strong> source, you will be asked to complete a survey',
    'SAMPLE_SOURCE_TYPE_HUMAN': 'Human',
    'SAMPLE_SOURCE_TYPE_ANIMAL': 'Animal',
    'SAMPLE_SOURCE_TYPE_ENVIRONMENTAL': 'Environmental',
    'UNCONSENTED_HEADER': 'Samples received but missing association with consent',
    'UNCONSENTED_EXPLANATION': 'The following samples have been received but have not been associated with a consent document. Please complete a survey if you have not, then <a href="%(sitebase)s/authed/add_sample_overview/">associate the sample</a>. <span style="font-weight:bold;color:red">We cannot process these samples until they are associated with a consent.</span>' % {'sitebase': media_locale['SITEBASE']},
    'SURVEY_HEADER_1': 'Survey',
    'SURVEY_TEXT_1': 'If you are taking a human or animal sample, we ask that you complete a survey.',
    'SURVEY_TEXT_2': 'The survey will take <strong>30-45 minutes</strong> for a human subject, or <strong>10 minutes</strong> for an animal subject. You <strong>cannot</strong> save in the middle of the survey, so please set aside enough time to complete the entire survey.',
    'SURVEY_TEXT_3': 'If you are taking a human sample, the survey includes demographic, lifestyle, medical and diet questions. All survey questions are optional.',
    'SURVEY_TEXT_4': 'The diet questions do not require a food diary, but please be prepared to answer questions about your eating habits. A screenshot of the dietary questions is shown below.',
    'SAMPLE_STEPS_HEADER_1': 'Before Taking Your Samples',
    'SAMPLE_STEPS_TEXT_1': 'These are the steps involved in taking a sample:',
    'SAMPLE_STEPS_TEXT_2': '<li>Make sure you have <a href="#" onclick="selectTab(\'source\')">added your sample source and complete the required survey(s)</a></li><li>Remove the sample swabs from the sample tube</li><li>Collect your sample following the guidelines below</li><li>Place sample swabs into the sample tube</li>',
    'SAMPLE_STEPS_TEXT_3': 'These sample collection instructions are very important, please read through them <strong>before</strong> beginning to take your sample. Deviations will cause issues with sample processing, sequencing, and data analysis. We cannot guarantee that we will be able to process your sample if the instructions are not followed, and <strong>we cannot offer replacements if instructions were not followed</strong>. Please do not hesitate to ask us questions at <a href="%(sitebase)s/authed/help_request/">%(help_email)s</a>.' % {"help_email": media_locale["HELP_EMAIL"], 'sitebase': media_locale['SITEBASE']},
    'SAMPLE_STEPS_HEADER_2': 'Taking Your Samples',
    'SAMPLE_STEPS_TEXT_4': 'Once you have removed the sample tube, only handle the sample swab by the red cap.',
    'SAMPLE_STEPS_TEXT_5': 'For a <strong>fecal sample</strong>, rub both cotton tips on a fecal specimen (a used piece ofbathroom tissue). Collect a small amount of biomass. Maximum collection would be to saturate 1/2 a swab. <strong>More is not better!</strong> The ideal amount of biomass collected is shown below.',
    'SAMPLE_STEPS_TEXT_6': 'For an <strong>oral sample</strong>, firmly rub both sides of both cotton tips on the surface of the tongue for 20 seconds. Take great caution not to touch the cheeks, teeth, or lips.',
    'SAMPLE_STEPS_TEXT_7': 'For a <strong>skin sample</strong>, firmly rub both sides of both cotton tips over the skin surface being sampled for 20 seconds.',
    'SAMPLE_STEPS_TEXT_8': 'For an <strong>other/environmental sample</strong>, firmly rub both sides of both cotton tips over the surface being sampled for 20 seconds.',
    'SAMPLE_STEPS_TEXT_9': 'After you have finished taking your sample, return the swabs to the sample tube and push the red cap on firmly.',
    'LOG_SAMPLE_HEADER_1': 'Logging Samples',
    'LOG_SAMPLE_TEXT_1': 'Please write the sample site, date, and time on the sampling tube.',
    'LOG_SAMPLE_TEXT_2': 'After writing the information on the sampling tube tube, <a href="%(sitebase)s/authed/add_sample_overview/">log the sample</a> in our system.' % {'sitebase': media_locale['SITEBASE']},
    'MAILING_HEADER_1': 'Mailing samples',
    'MAILING_TEXT_1': 'Once you have added a <a href="#" onclick="selectTab(\'source\')">sample source, completed the relevant survey</a> (if applicable), <a href="#" onclick="selectTab(\'sample\')">taken</a> and <a href="#" onclick="selectTab(\'log\')">logged your samples</a>, you should then mail the samples back to us.',
    'MAILING_TEXT_2': 'Wrap the sample tube in absorbent tissue, such as facial tissue or paper towels, and mail it back as soon as possible. The absorbent tissue will help to keep the relative humidity within the package low.',
    'MAILING_TEXT_3': 'We also recommend using a reinforced envelope to reduce the chance of losing your sample due to damaged packaging.',
    'MAILING_TEXT_4': 'The sooner we receive your sample, the sooner we can get it stored in our -80C freezers and ready for processing!',
    'MAILING_TEXT_5': '<strong>Do not refrigerate or freeze the samples</strong> if they cannot be shipped immediately. Store them in a cool dry place such as a cabinet or a closet.',
    'DOMESTIC_HEADER_1': 'Domestic Shipping',
    'DOMESTIC_TEXT_1': 'Shipping within the US should be less than $1.50, but we recommend taking the sample to the post office to get the proper postage. Getting the postage right on the first try is important since samples that spend a long time in transit will likely not produce the highest quality results.',
    'DOMESTIC_TEXT_2': 'This is the shipping address:',
    'DOMESTIC_TEXT_3': media_locale['SHIPPING_ADDRESS'],
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
    'RESULTS_READY_TEXT_1': 'One or more of the samples you submitted have been sequenced, and the results are now available online! Currently, we have only processed fecal samples, but we will be processing samples from other body sites soon.',
    'RESULTS_READY_TEXT_2': 'To access your available results, hover over "Human Samples" in the menu on the left, hover over your name, then click on your sample to view your results, or click one of the links below. <b>For help interpreting results, <a href="%s/authed/addendum/">click here</a></b>. The following barcodes are ready:' % _SITEBASE,
    'RESULTS_READY_TEXT_3': 'You will be able to view your results here on this website once they are available.'
}

_CHANGE_PASS_VERIFY = {
    'TITLE': 'Please enter new password',
    'NEW_PASSWORD': 'New Password',
    'HELP_NEW_PASSWORD': 'The new password you would like to use to log in from now on.',
    'CONFIRM_PASSWORD': 'Confirm Password',
    'HELP_CONFIRM_PASSWORD': "Repeat your New Password again, exactly as before. We ask you to repeat it here so that you don't accidentally change your password to something you did not intend.",
    'BUTTON_TEXT': 'Change Password',
    'NO_VALID_CODE': 'Your password change code is not valid. If you wish to change your password please <a href="%(sitebase)s/forgot_password/">start over</a>' % {'sitebase': media_locale['SITEBASE']},
    'SUCCESS': 'Your password has been changed',
    'NO_EMAIL_1': 'Could not send Email',
    'NO_EMAIL_2': 'We attempted to email the message below:',
    'NO_EMAIL_3': 'This is a courtesy email to confirm that you have changed your password for your kit with ID %(kitid)s If you did not request this change, please email us immediately at %(help_email)s.'
}

# helper tuples for the survey questions
_NO_RESPONSE_CHOICE = "Unspecified"
_YES_NO_CHOICES = (_NO_RESPONSE_CHOICE, 'Yes', 'No')
_YES_NO_NOTSURE_CHOICES = (_NO_RESPONSE_CHOICE, 'Yes', 'No', 'Not sure')
_FREQUENCY_MONTH_CHOICES = (_NO_RESPONSE_CHOICE,
                            'Never',
                            'Rarely (a few times/month)',
                            'Occasionally (1-2 times/week)',
                            'Regularly (3-5 times/week)',
                            'Daily')
_FREQUENCY_WEEK_CHOICES = (_NO_RESPONSE_CHOICE,
                           'Never',
                           'Rarely (less than once/week)',
                           'Occasionally (1-2 times/week)',
                           'Regularly (3-5 times/week)',
                           'Daily')
_DIAGNOSIS_CHOICE = (_NO_RESPONSE_CHOICE,
                     'I do not have this condition',
                     'Diagnosed by a medical professional (doctor, physician assistant)',
                     'Diagnosed by an alternative medicine practitioner',
                     'Self-diagnosed')

_ANIMAL_SURVEY = {
    'GENERAL_TITLE': 'General',
    'GENERAL_QUESTION_1': 'Animal type?',
    'GENERAL_QUESTION_1_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Dog',
                                   'Cat',
                                   'Small mammal',
                                   'Large mammal',
                                   'Fish',
                                   'Bird',
                                   'Reptile',
                                   'Amphibian',
                                   'Other'),

    'GENERAL_QUESTION_2': 'Origin?',
    'GENERAL_QUESTION_2_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Breeder',
                                   'Shelter',
                                   'Home',
                                   'Wild'),

    'GENERAL_QUESTION_3': 'Age?',
    'GENERAL_QUESTION_3_CHOICES': None,

    'GENERAL_QUESTION_4': 'Gender?',
    'GENERAL_QUESTION_4_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Male',
                                   'Female',
                                   'Unknown'),

    'GENERAL_QUESTION_5': 'Setting?',
    'GENERAL_QUESTION_5_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Urban',
                                   'Suburban',
                                   'Rural'),

    'GENERAL_QUESTION_6': 'Weight category?',
    'GENERAL_QUESTION_6_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Underweight',
                                   'Skinny',
                                   'Normal',
                                   'Chubby',
                                   'Overweight'),

    'GENERAL_QUESTION_7': 'Diet classification?',
    'GENERAL_QUESTION_7_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Carnivore',
                                   'Omnivore',
                                   'Herbivore'),

    'GENERAL_QUESTION_8': 'Food source?',
    'GENERAL_QUESTION_8_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'Pet store food',
                                   'Human food',
                                   'Wild food'),

    'GENERAL_QUESTION_9': 'Food type?',
    'GENERAL_QUESTION_9_CHOICES': (_NO_RESPONSE_CHOICE,
                                   'dry',
                                   'wet',
                                   'both'),

    'GENERAL_QUESTION_10': 'Food special attributes?',
    'GENERAL_QUESTION_10_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'Organic',
                                    'Grain free'),

    'GENERAL_QUESTION_11': 'Social?',
    'GENERAL_QUESTION_11_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'Lives alone with humans',
                                    'Lives alone no/limited humans (shelter)',
                                    'Lives with other animals and humans',
                                    'Lives with other animals/limited humans'),

    'GENERAL_QUESTION_12': 'Any pets the current animal lives with?',
    'GENERAL_QUESTION_12_CHOICES': None,

    'GENERAL_QUESTION_13': 'Add the age of any human that the current animal lives with',
    'GENERAL_QUESTION_13_CHOICES': None,

    'GENERAL_QUESTION_14': 'Add the gender of any human that the current animal lives with',
    'GENERAL_QUESTION_14_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'Male',
                                    'Female',
                                    'Other'),

    'GENERAL_QUESTION_15': 'Hours spent outside?',
    'GENERAL_QUESTION_15_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'None',
                                    'Less than 2',
                                    '2-4',
                                    '4-8',
                                    '8+'),

    'GENERAL_QUESTION_16': 'Toilet water access?',
    'GENERAL_QUESTION_16_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'Regular',
                                    'Sometimes',
                                    'Never'),

    'GENERAL_QUESTION_17': 'Coprophage?',
    'GENERAL_QUESTION_17_CHOICES': (_NO_RESPONSE_CHOICE,
                                    'High',
                                    'Moderate',
                                    'Low',
                                    'Never'),

    'SUPPLEMENTAL_COMMENTS': 'Please write anything else about this animal that you think might affect its microorganisms.'
}

_HUMAN_SURVEY_COMPLETED = {
    'COMPLETED_HEADER': 'Congratulations!',
    'COMPLETED_TEXT': 'You are now an enrolled participant in the %(PROJECT_TITLE)s! As a reminder, you still need to associate your sample(s) with the survey to complete the process. If your sample(s) are not associated with a survey, we will not be able to process them.' % media_locale,
    'AVAILABLE_SURVEYS': 'Below are a few additional surveys that you may be interested in completing. There is no requirement to take these surveys, and your decision does not affect your involvement in the project in any way.',
    'SURVEY_ASD': '<h3 style="text-align: center"><a href="%s" target="_blank">ASD-Cohort survey</a></h3><a href="http://www.anl.gov/contributors/jack-gilbert">Dr. Jack Gilbert</a> is exploring the relationship between gut dysbiosis and Autism Spectrum Disorders, and in conjunction with the American Gut Project, we started an ASD-Cohort study. This additional survey contains questions specific to that cohort, but it is open to any participant to take if they so choose.',
    'SURVEY_VIOSCREEN': '<h3 style="text-align: center"><a href="%s" target="_blank">Dietary Survey</a></h3>The American Gut Project and its sister projects are very interested in diet. If you\'d like to provide additional detail about your diet, please click the link above to take a detailed diet survey (known as an Food Frequency Questionnaire). This is a validated FFQ, and is the one used by the Mayo Clinic.',
    'SURVEY_FERMENTED': '<h3 style="text-align: center"><a href="%s" target="_blank">Fermented Foods Survey</a></h3>As part of our onging research into what drive changes in the human gut microbiome, we are looking at fermented foods and the microbiomes of fermented food eaters. Please click the link above if you would like to participate in this survey.',
    'SURVEY_SURF': '<h3 style="text-align: center"><a href="%s" target="_blank">Surfing Survey</a></h3>As part of our study, we are interested in the effects of frequent and prolonged exposure to salt water and the ocean, as it pertains to surfing and surfers. If you are interested in participating, you can click the link above and take the survey.',
}

_SURVEY_MAIN = {
    'TITLE': 'Survey',
    'ONCE_YOU_START': 'Once you start this survey, you must complete it. Your answers will <strong>not</strong> be saved unless you complete the entire survey.',
    'TIME_COMMITMENT': 'We anticipate that participant time commitment for completing the questionnaire online will take no more than <strong>45 minutes</strong>.',
    'TYPES_OF_QUESTIONS': 'You will be asked questions about your general personal information (name, age, sex, height, weight, ethnicity, place of birth, and current ZIP or equivalent code). We will ask if you recently moved and where you moved from. We will ask questions about general diet information (including whether you follow a special diet, if you have food allergies, whether you have cultural or religious food restrictions). Other questions address whether you have pets and the type of contact you have with these pets and your relationship to other people in this study.  There is a section on health information including a history of allergies/asthma, if you suffer from migraines and if you have a history of irritable bowel disease.',
    'YOU_MAY_DECLINE': 'You may decline to answer any question by not selecting an answer.',
    'OTHER_SURVEYS': 'Following the questionnaire, you will be presented with a few other focused surveys. As with everything, those surveys are optional but your responses could help improve our understanding of the microbiome.'
}

_NOJS = {
    'MESSAGE': 'You have JavaScript disabled, which this site requires in order to function properly. <br/>Please enable javascript and reload <a href="http://www.microbio.me/americangut">http://www.microbio.me/americangut</a>.',
    'NEED_HELP': 'If you need help enabling JavaScript in your browser, <br/>Please email us at <a href="mailto:americangut@gmail.com">americangut@gmail.com</a>'
}

_PERSONAL_MICROBIOME = {
    'HEADER': 'Online Survey Consent Form',
    'CONSENT_1': 'You are being invited to participate in a research study titled "Impact of Personal Microbiome Information on American Gut Study Volunteers." This study is being done by Dr. Cinnamon Bloss, Professor from the University of California - San Diego (UCSD) School of Medicine. You are being invited to participate in this research because you took part in the American Gut Project study.',
    'CONSENT_2': "The purpose of this research study is to better understand how participation in the American Gut Project may have impacted people's health views, health behaviors, or communication with their healthcare provider. If you agree to take part in this study the following will happen to you:",
    'CONSENT_LIST_1': 'You will complete an online survey. This survey will ask questions about how you feel about your experience in the American Gut Project, about the impact receiving your personal microbiome results has on you, and some demographic questions about you. It will take about 5-10 minutes to complete the survey.',
    'CONSENT_LIST_2': 'Information that you provided as part of the American Gut Project will be collected and used in this study.',
    'CONSENT_LIST_3': "The study may also involve follow up interviews at a later date to collect more detailed and specific information about how participation in the American Gut Project has impacted participant's health. If you would like to participate in the possible follow-up interviews to share more of your thoughts, you can provide your contact information at the end of the survey. However, you should note that, even if you agree to be interviewed it is possible that you will not be contacted.",
    'CONSENT_3': "The data collected as part of this study may also be used in studies by other researchers from UCSD and other Universities. Dr. Bloss will be responsible for deciding how your data will be used. Dr. Bloss, her associates, or her successors in these studies will keep your data and the information derived from it for an indefinite period. By consenting to participate in this study you are indicating that you consent to the use of your data in other studies. If you do not consent to such use you should not participate in this study.",
    'CONSENT_4': "There will not be any direct benefit to you from this research. The investigator(s), however, may better understand how participating in the American Gut Project impacts people's health views, health behaviors, and communication with their healthcare providers.",
    'CONSENT_5': "There are minimal risks associated with this research study. Taking surveys can produce feelings of stress, frustration, discomfort, fatigue, and boredom.  To limit these risks, the questions have been written in a clear manner. There is a risk of loss of confidentiality. To protect against such a loss research records will be kept confidential to the extent allowed by law. Your survey data will be stored on a password protected secure computer will be identified by a study subject ID number.  If you decide to provide your name and contact information for potential follow-up, your name and contact information will be kept separate from your survey responses and will not be linked to your survey responses.  All analysis of the survey data will be done on data that is de-identified (e.g. does not contain your name). Research records may be reviewed by the UCSD Institutional Review Board and the National Institutes of Health. Results of this study may be reported in scientific journals, meeting, and news media, but none of these reports will use your name or use data that can point to any person who took part in the study.",
    'CONSENT_6': "Your participation in this study is completely voluntary and you can withdraw at any time by simply exiting the survey. Choosing not to participate or withdrawing will result in no penalty or loss of benefits to which you are entitled. You are free to skip any question that you choose.",
    'CONSENT_7': "If you have questions about this project or if you have a research-related problem, you may contact the researcher(s), Dr. Cinnamon Bloss at 858-534-9550. If you have any questions concerning your rights as a research subject, you may contact the UCSD Human Research Protections Program Office at (858) 246-7444.",
    'CONSENT_8': 'By clicking "You agree" below you are indicating that you are at least 18 years old, have read this consent form, and agree to participate in this research study. Please print a copy of this page for your records.',
    'AGREE': 'You Agree',
    'DISAGREE': 'You Do Not Agree'
}

# Actual text locale
text_locale = {
    'nojs.html': _NOJS,
    '404.html': _404,
    '403.html': _403,
    'FAQ.html': _FAQ,
    'interactive_categories': _INTERACTIVE_CATEGORIES,
    'taxa.html': _INTERACTIVE_MULTIPLE,
    'new_participant_overview.html': _NEW_PARTICIPANT_OVERVIEW,
    'personal_microbiome_overview.html': _PERSONAL_MICROBIOME,
    'addendum.html': _ADDENDUM,
    'portal.html': _PORTAL,
    'db_error.html': _DB_ERROR,
    'retrieve_kitid.html': _RETREIVE_KITID,
    'add_sample.html': _ADD_SAMPLE,
    'error.html': _ERROR,
    'forgot_password.html': _FORGOT_PASSWORD,
    'help_request.html': _HELP_REQUEST,
    'new_participant.html': _NEW_PARTICIPANT,
    'international.html': _INTERNATIONAL,
    'add_sample_overview.html': _ADD_SAMPLE_OVERVIEW,
    'participant_overview.html': _PARTICIPANT_OVERVIEW,
    'sample_overview.html': _SAMPLE_OVERVIEW,
    'taxa_summary.html': _TAXA_SUMMARY,
    'map.html': _MAP,
    'human_survey_completed.html': _HUMAN_SURVEY_COMPLETED,
    'register_user.html': _REGISTER_USER,
    'chage_pass_verify.html': _CHANGE_PASS_VERIFY,
    'survey_main.html': _SURVEY_MAIN,
    'animal_survey.html': _ANIMAL_SURVEY,
    'handlers': _HANDLERS
}
