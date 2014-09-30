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
media_locale = {
    'LOGO': '/static/img/ag_logo.jpg',
    'STEPS_VIDEO': "http://player.vimeo.com/video/63542787",
    'FOOD_LOG': 'http://player.vimeo.com/video/63926337',
    'ADD_PARTICIPANT': 'http://player.vimeo.com/video/63931218',
    'ADD_PARTICIPANT_IMG_1': "/static/img/add_participant.png",
    'ADD_PARTICIPANT_IMG_MENU': "/static/img/add_participant_menu.png",
    'LOG_SAMPLE_OPTS': "/static/img/log_sample_options.png",
    'ADD_SAMPLE_HIGHLIGHT': "/static/img/add_sample_highlight.png",
    'ADD_SAMPLE_OVERVIEW': "/static/img/add_sample_overview.png",
    'FAQ_AMBIGUOUS_PASS': '/static/img/creds_example.png',
    'SAMPLE_BARCODE': '/static/img/sample_barcode.jpg',
    'SWAB_HANDLING': 'http://player.vimeo.com/video/62393487',
    'HELP_EMAIL': 'info@americangut.org',
    'PROJECT_TITLE': AMGUT_CONFIG.project_name,
    'FAVICON': '/static/img/favicon.ico',
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
    'NAV_LOG_SAMPLE': 'Log Sample',
    'NAV_JOIN_PROJECT': 'Join The Project',
    'NAV_KIT_INSTRUCTIONS': 'Kit Instructions',
    'NAV_PARTICIPANT_LOGIN': 'Participant Log In',
    'NAV_FORGOT_KITID': 'I forgot my kit ID',
    'NAV_FORGOT_PASSWORD': 'I forgot my password'
}

# Template specific dicts
_FAQ = {
    'FAQ_HEADER': "%(shorthand)s FAQ" % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'LOG_IN_WHAT_NOW_ANS_1': 'You need to follow the add participant workflow. Click on the "Add Source & Survey" tab located at the top of the page.',
    'INFORMATION_IDENTIFY_ME': 'Can data describing my gut microbiome be used to identify me or a medical condition I have?',
    'LOG_IN_WHAT_NOW_ANS_3': 'You can log a sample by clicking the "Log Sample" link in the menu. If you do not see the "Log Sample" link, then all of your barcodes have been assigned.',
    'PARTICIPATE_WITH_DIAGNOSIS': 'Can I participate in the project if I am diagnosed with ...?',
    'LOG_IN_WHAT_NOW_ANS_5': 'When adding a sample, please be sure to select the barcodes that matches the barcode on the sampling tube of the sample that you are logging',
    'CONVERT_GRAMS_CALORIES': 'How do I convert grams of macronutrients into percentage of calories?',
    'TAKES_SIX_MONTHS': 'Does it really take up to 6 months to get my results?',
    'HOW_CHANGE_GUT': 'How can I change my gut microbiome?',
    'FOOD_DIARY_ANS': 'In fact, responses to all questions on the survey, including the dietary questions, are strictly voluntary. Technically you are not required to provide all those information, but it is <em>highly recommended</em>. Having the information will help us make possible connections from your life styles to your microbe living on/within you and hopefully figure out how that can impact your health. Particularly, we know diet is a major factor affecting the gut microbiome since our gut microbes eat the food we don\xe2\x80\x99t digest. Having diet information will allow us to look for patterns in gut microbiome composition across populations of people with different diets.',
    'BETTER_OR_WORSE': 'How can I tell if my gut microbiome is better or worse than other people in my category?',
    'ONLY_FECAL_RESULTS_ANS': 'We have only sent out results for fecal samples and are in the process of evaluating how best to present the other sample types. Please see <a href="#faq12">the previous question </a>',
    'DIFFERENT_WHATS_WRONG_WITH_ME_ANS': 'No! Your gut microbiome is as unique as your fingerprint so you should expect to see some differences. Many factors can affect your gut microbiome, and any differences you see are likely to be the result of one of these factors. Maybe your diet is different than most people your age. Maybe you just traveled somewhere exotic. Different does not necessarily mean bad.',
    'WHEN_RESULTS_NON_FECAL_ANS': 'The vast majority of the samples we\xe2\x80\x99ve received are fecal, which was why we prioritized those samples. Much of the analysis and results infrastructure we\xe2\x80\x99ve put in place is applicable to other sample types, but we do still need to assess what specific representations of the data make the most sense to return to participants. We apologize for the delay. Our tentative goal for skin and oral samples is January 1st, 2014, and environmental samples sometime during the first quarter of 2014.',
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
    'RAW_DATA_ANS_1': '<P>The raw data can be fetched from the <a href=http://www.ebi.ac.uk/>European Bioinformatics Institute</a>. EBI is part of <a href=http://www.insdc.org/>The International Nucleotide Sequence Database Collaboration</a> and is a public warehouse for sequence data. The deposited %(project)s accessions so far are:<ol><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP003819&display=html">ERP003819</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP003822&display=html">ERP003822</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP003820&display=html">ERP003820</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP003821&display=html">ERP003821</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP005367&display=html">ERP005367</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP005366&display=html">ERP005366</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP005361&display=html">ERP005361</a></li><li style="list-style-type:square"><a href="http://www.ebi.ac.uk/ena/data/view/ERP005362&display=html">ERP005362</a></li></ol>' % {"project": AMGUT_CONFIG.project_name},
    'BETTER_OR_WORSE_ANS': 'Right now, you can\xe2\x80\x99t. We\xe2\x80\x99re still trying to understand what constitutes a normal or average gut microbiome, and we have a lot to learn about the functions of many of the microbes that inhabit the gut. Therefore, it\xe2\x80\x99s tough to know what combinations of microbes are best for nutrition and health. That\xe2\x80\x99s one reason collecting data from so many people is important\xe2\x80\x94hopefully we can start to learn more about this.',
    'LOOK_BELOW': "If you're still experiencing issues, look for your problem in the FAQ below",
    'PASSWORD_SAME_VERIFICATION_ANS': 'No. Your <strong>password</strong> is printed on the sheet that you received with your kit in the mail. That sheet looks like this:</p>'
                                '<img src="%(FAQ_AMBIGUOUS_PASS)s"/><p>Your <strong>verification code</strong> is emailed to you. Look for the email: <br /><br /><strong>FROM:</strong>  %(project)s (info@americangut.org)<br /><strong>SUBJECT:</strong>  %(shorthand)s Kit ID & Verification Code' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name, "FAQ_AMBIGUOUS_PASS": media_locale['FAQ_AMBIGUOUS_PASS']},
    'TAKES_SIX_MONTHS_ANS': 'Yes. It takes about 8 weeks for extractions, 8 weeks for the remainder of the processing, and 2 weeks to do the actual sequencing. This is before any analysis and if everything goes as planned, with no delays - equipment down, run failures, reagents or other consumables back ordered. Things do sometimes go wrong, so we say up to 6 months.',
    'PARTICIPATE_WITH_DIAGNOSIS_ANS': 'Of course! The only exclusion criteria are: you must be more than 6 weeks old and cannot be a convicted felon. Please keep in mind that, for legal and ethical reasons, the %(project)s does not provide medically actionable results or advice.' % {"project": AMGUT_CONFIG.project_name},
    'HOW_PROCESS_SAMPLES': 'How are the samples and data processed?',
    'WHO_MICHAEL_POLLAN_ANS': 'Michael Pollan is a New York Times Best Seller for his books on diet and nutrition. Further information about Michael can be found <a href="http://michaelpollan.com/">here</a>.',
    'WHO_MICHAEL_POLLAN': 'Who is Michael Pollan?',
    'HOW_CHANGE_GUT_ANS': 'Although we still don\xe2\x80\x99t have a predictable way to change the gut microbiome in terms of increasing or decreasing the abundances of specific bacteria, we do know that a variety of factors influence gut microbial community composition. Diet is a major factor affecting the gut microbiome so by changing your diet, you may be able to affect your gut microbiome. We still don\xe2\x80\x99t fully understand probiotics but know that they can influence your gut microbiome while you are actively taking them. Factors such as stress can also influence the gut microbiome. However, it is important to remember that there are factors we can\xe2\x80\x99t change, such as age or genetics, that can affect the gut microbiome.',
    'RAW_DATA': 'How can I get the raw data?',
    'WATCH_VIDEOS': "Watch these helpful videos about what to do once you've received your kit!",
    'INTRODUCTION_BEGINNING': '<a href="http://www.robrdunn.com">Rob Dunn</a> has provided this excellent introduction to some of the basics that every curious reader should check out!<br/>&nbsp;<br/>Rob is the author of the <a href="http://www.yourwildlife.org/the-wild-life-of-our-bodies/">Wild Life of Our Bodies</a>. He is an evolutionary biologist and writer at North Carolina State University. For more about your gut and all of your other parts, read more from Rob at <a href="http://www.robrdunn.com">www.robrdunn.com</a></p>'
                                '',
    'INFORMATION_IDENTIFY_ME_ANS': 'No. First, all of your personal information has been de-identified in our database as mandated by institutional guidelines. Second, although each person has a unique gut microbiome, many of the unique qualities are at the species or strain level of bacteria. Our sequencing methods currently do not allow us to describe your gut microbiome in that much detail. Finally, for most medical conditions, there are no known, predictable patterns in gut microbial community composition. Research simply hasn\xe2\x80\x99t gotten that far yet.</p>'
                                '<p>We should also mention that since we are only interested in your microbes, we do not sequence human genomic DNA in our typical analyses. Where it is possible for human DNA to be sequenced (e.g., the Beyond Bacteria kits), we remove the human DNA using the same bioinformatics approaches undertaken in the NIH-funded Human Microbiome Project and approved by NIH bioethicists. Additionally, there is so little human DNA in fecal, skin and mucus samples that the chances of us being able to sequence your entire human genome are almost none, even if we tried.',
    'FECAL_NO_RESULTS_ANS': 'On any given sequencing run (not just the %(shorthand)s), a small percentage of the samples fail for unknown reasons -- our methods are good but not perfect. This is one of the reasons the sample kits have two Q-tips. It allows us to perform a second microbial DNA extraction and re-sequence if the first attempt failed. We will be doing this for all of the samples that failed. If there was a technical problem with the sample itself (e.g. not enough microbes on the swab) that inhibits us from producing data for you, we will be re-contacting you about collecting another sample.' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'MULTIPLE_KITS_DIFFERENT_TIMES_ANS': 'For best results, we recommend that you mail each sample within 24 hours of collection.',
    'STEPS_TO_FOLLOW': '<a href="%(video)s">%(shorthand)s - Steps to Follow When Your Kit Arrives</a> from <a href="http://vimeo.com/user16100300">shelley schlender</a> on <a href="http://vimeo.com">Vimeo</a>.' % {"shorthand": AMGUT_CONFIG.project_shorthand, "video": media_locale["STEPS_VIDEO"]},
    'WHY_TWO_SWABS': 'Why are there 2 swabs inside the tube?',
    'MULTIPLE_KITS_DIFFERENT_TIMES': ' have a 2+ sample kit, and would like to collect and send them in at different times',
    'FOOD_DIARY': 'Why am I asked for a seven-day food diary? Do I really need to fill the survey?',
    'COMBINE_RESULTS_ANS': "We're still evaluating how best to present the data for samples that represent a family. We are mailing individual results now and will provide updated results through the web site later.",
    'PASSWORD_SAME_VERIFICATION': 'Is my password the same as my verification code?',
    'FECAL_NO_RESULTS': 'I sent in a fecal sample but did not get any results, what happened to them?',
    'CONVERT_GRAMS_CALORIES_ANS': 'Once you determine how many grams of protein, carbohydrates and lipids you have consumed each day, multiply the grams of protein and the grams of carbohydrates by 4 each (since there are 4 calories in every gram of protein and carbohydrate) and multiply the grams of lipids by 9 (since there are 9 calories in every gram of lipids). Add all of these numbers together to determine the total number of calories you consumed. Divide protein calories by the total calories to determine the percentage of calories consumed as protein. Repeat for carbohydrates and lipids.',
    'DIFFERENT_WHATS_WRONG_WITH_ME': "I'm different than other people in my category. Does that mean something is wrong with me?",
    'WHY_TWO_SWABS_ANS_2': "<P>Each tube is used for <strong>one sample</strong>. The tube has two swabs in it because one is a backup in case the DNA does not amplify on the first swab.</p>"
                           "<p>Here's a video of Rob Knight talking about swab handling:</p>"
                           "<iframe src='%(swab_handling)s' width=''500'' height=''281'' frameborder=''0'' webkitallowfullscreen='' mozallowfullscreen='' allowfullscreen=''></iframe>" % {'swab_handling': media_locale['SWAB_HANDLING']},
    'MISSING_METADATA_ANS': 'Metadata are information describing your age, gender, diet, etc. Missing metadata mean that this person did not provide us with this information.',
    'WHERE_SEND_SAMPLE': 'Where do I send my sample?',
    'VARIABLE': 'TEXT',
    'LOG_IN_WHAT_NOW': "I'm logged in, what do I do now?",
    'LOG_IN_WHAT_NOW_ANS_2': '<p>During this workflow you (or whomever is being sampled) will:</p>'
                                '<ol>   <li>Add a participant</li><li>Provide electronic consent</li><li>Answer survey questions (including the diet questions covered by the food diary)</li><li>Upon completion, become eligible to log samples</li>          </ol><p>When participants are eligible,  you will then see their name under the corresponding menu on the left, in this example we have just added the participant "Test":</p>'
                                '',
    'PROJECT_101': '%(shorthand)s 101' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'WHAT_FORMS_ANS': 'The instruction on the sampling instructions that requires you to "place your forms and the sample tube in preaddressed envelope" is leftover from a previous version of the sampling instructions. There are no forms for you to include inside the envelope with your sample. If you are shipping internationally, please visit the <a href="/international_shipping/">International Shipping Instructions</a></p>'
                                '',
    'WHY_TWO_SWABS_ANS_1': 'Each sampling tube contains two swabs and looks like this:',
    'MISSING_METADATA': 'What are missing metadata?',
    'ONLY_FECAL_RESULTS': 'I sent more than one kind of sample, but I only received data for my fecal sample. What happened to my other samples?',
    'NOT_A_BUSINESS_ANS': 'We have had many enquiries about our "service" or "business". %(shorthand)s is a donation-supported academic project that is a collaboration between the <a href="http://www.earthmicrobiome.org">Earth Microbiome Project</a> and the <a href="http://humanfoodproject.com/">Human Food Project</a>, primarily run out of the <a href="https://knightlab.colorado.edu/">Knight Lab</a> at the University of Colorado at Boulder, and is not a business or service.  In particular, %(shorthand)s is not a diagnostic test (although the information gained through the project may in future contribute to the development of diagnostic tests). All data except for information that needs to be kept confidential for privacy reasons is openly and freely released into public databases, and the project is not intended to make a profit (any surplus funds would be recycled back into furthering human microbiome research).' % {"shorthand": AMGUT_CONFIG.project_shorthand},
    'LOG_FOOD': '<a href="%(food_log_vid)s">%(shorthand)s - How to Log Food</a> from <a href="http://vimeo.com/user16100300">shelley schlender</a> on <a href="http://vimeo.com">Vimeo</a>.' % {'food_log_vid': media_locale["FOOD_LOG"], 'shorthand': AMGUT_CONFIG.project_shorthand},
    'HOW_PROCESS_SAMPLES_ANS': 'The majority of the samples in the %(project)s are run through a processing pipeline designed to amplify a small region of a gene that is believed to be common to all Bacteria and Archaea. This gene, the 16S ribosomal RNA gene is like a barcode you find on your groceries, and serves as a marker for different organisms. There are quite a few different ways to assess the types of Bacteria and Archaea in a sample, including a variety of techniques even to look at this single gene. Every method has its biases, and comparing data between different methods is <a href="http://www.ncbi.nlm.nih.gov/pubmed/23861384">non-trivial</a> and can sometimes be nearly impossible. One of the primary goals of the %(shorthand)s is to provide data that can be used and reused by researchers worldwide, we have opted to use the standard protocols adopted by the <a href="http://earthmicrobiome.org">Earth Microbiome Project</a>, (<a href="http://www.ncbi.nlm.nih.gov/pubmed/22402401">Caporaso et al 2012</a>, and more detailed description of the <a href="http://www.earthmicrobiome.org/emp-standard-protocols/16s/">protocol</a>). This ensures that the data generated by the %(shorthand)s can be combined with the other 80,000 samples so far indexed by the EMP (as scientists, we get giddy about things like this).</p>'
                                '<p>DNA sequencing is a complex challenge that involves an army of robots, ultra pure water that costs $75 per 10ml, and an amazing <a href="http://www.illumina.com/systems/miseq.ilmn">digital camera</a> that actually determines individual sequences one nucleotide at a time. The number of stunningly brilliant minds whose footprints exist in these methods is astounding. However, the challenges don\xe2\x80\x99t end once you get the DNA sequence - some might say they are just beginning. It turns out that figuring out what actually is in your sample, that is, what organisms these sequences correspond to, requires cutting edge computational approaches, supercomputers and caffeine for the people operating them. The questions being asked of the data are themselves complex, and volume of data being processed is simply phenomenal. To give you some idea, for each sample sequenced we obtain around 6 million nucleotides which we represent as letters (A, T, G or C, see <a href="http://en.wikipedia.org/wiki/Nucleotide">here</a> for more info), whereas Shakespeare\'s Hamlet only contains around 150,000 letters (ignoring spaces).</p>'
                                ' <p>The primary software package we use for processing 16S sequence data is called Quantitative Insights into Microbial Ecology (<a href="http://www.qiime.org">QIIME</a>; <a href="http://www.ncbi.nlm.nih.gov/pubmed/20383131">Caporaso et al. 2010</a>). Using this package, we are able to start with raw sequence data and process it to so that we end up be able to  explore the relationships within and between samples using a variety of statistical methods and metrics. To help in the process, we leverage a standard and comprehensive (to date) reference database called Greengenes (<a href="http://www.ncbi.nlm.nih.gov/pubmed/22134646">McDonald  et al. 2011</a>; <a href="http://www.ncbi.nlm.nih.gov/pubmed/16820507">DeSantis et al. 2006</a>) that includes information on a few hundred thousand Bacteria and Archaea (it is likely that there are millions or more species of bacteria). Due to the molecular limitations of our approach, and the lack of a complete reference database (because the total diversity of microbes on Earth is still unknown), our ability to determine whether a specific organism is present has a margin of error on the order of millions of years, which limits our ability to assess specific strains or even species using this inexpensive technique (more expensive techniques, such as some of the higher-level perks, can provide this information). But all is not lost! By using the evolutionary history of the organisms as inferred by the small pieces of DNA that we have, we can begin to ask broad questions about the diversity within (see <a href="http://www.ncbi.nlm.nih.gov/pubmed/7972354">Faith 1994</a>) and between samples (see <a href="http://www.ncbi.nlm.nih.gov/pubmed/16332807">Lozupone and Knight 2005</a>), and whether the patterns observed relate to study variables (e.g., BMI, exercise frequency, etc).</p>'
                                ' <p>The specifics on how the %(shorthand)s sequence data are processed can be found <a href="http://nbviewer.ipython.org/github/biocore/American-Gut/blob/master/ipynb/module2_v1.0.ipynb">here</a>, and are written up in an executable <a href="http://ipython.org/notebook">IPython Notebook</a>, which provides all the relevant processing steps in an open-source format. Be warned, processing the full %(shorthand)s dataset takes over 5,000 CPU hours right now (i.e. if you do it on your laptop it might take 7 months, even if you don\xe2\x80\x99t run out of memory: this might put the time it takes to get your results in perspective). This is the processing pipeline that we use on your data. As this project is a work in progress, we are versioning the processing pipeline as there will continue to be improvements to the process as the project moves forward.</p>'
                                ' <p>Additional information about the tools used in the %(project)s and our contributions to the microbiome community can be found in the following publications:</p>'
                                ' <ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21552244">Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24280061">EMPeror: a tool for visualizing high-throughput microbial community data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16332807">UniFrac: a new phylogenetic method for comparing microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16893466">UniFrac--an online tool for comparing microbial community diversity in a phylogenetic context.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17220268">Quantitative and qualitative beta diversity measures lead to different insights into factors that structure microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/19710709">Fast UniFrac: facilitating high-throughput phylogenetic analyses of microbial communities including analysis of pyrosequencing and PhyloChip data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20827291">UniFrac: an effective distance metric for microbial community comparison.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21885731">Linking long-term dietary patterns with gut microbial enterotypes.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23326225">A guide to enterotypes across the human body: meta-analysis of microbial community structures in human microbiome datasets.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699609">Structure, function and diversity of the healthy human microbiome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699610">A framework for human microbiome research.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23587224">The Biological Observation Matrix (BIOM) format or: how I learned to stop worrying and love the ome-ome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22134646">An improved Greengenes taxonomy with explicit ranks for ecological and evolutionary analyses of bacteria and archaea.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304728">The Earth Microbiome Project: Meeting report of the "1 EMP meeting on sample selection and acquisition" at Argonne National Laboratory October 6 2010.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304727">Meeting report: the terabase metagenomics workshop and the vision of an Earth microbiome project.</a></li> </ul> <p>More detail on our work on the effects of storage conditions can be found in these publications:</p>'
                                ' <ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20412303">Effect of storage conditions on the assessment of bacterial community structure in soil and human-associated samples.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20673359">Sampling and pyrosequencing methods for characterizing bacterial communities in the human gut using 16S sequence tags.</a></li> </ul> <p>And more detail on our work on sequencing and data analysis protocols can be found in these publications:</p>'
                                ' <ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17881377">Short pyrosequencing reads suffice for accurate microbial community analysis.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18723574">Accurate taxonomy assignments from 16S rRNA sequences produced by highly parallel pyrosequencers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18264105">Error-correcting barcoded primers for pyrosequencing hundreds of samples in multiplex.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22237546">Selection of primers for optimal taxonomic classification of environmental 16S rRNA gene sequences.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22170427">Comparison of Illumina paired-end and single-direction sequencing for microbial 16S rRNA gene amplicon surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21716311">Impact of training sets on classification of high-throughput bacterial 16s rRNA gene surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21349862">PrimerProspector: de novo design and taxonomic analysis of barcoded polymerase chain reaction primers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20383131">QIIME allows analysis of high-throughput community sequencing data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22161565">Using QIIME to analyze 16S rRNA gene sequences from microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23861384">Meta-analyses of studies of the human microbiota.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24060131">Advancing our understanding of the human microbiome using QIIME.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20534432">Global patterns of 16S rRNA diversity at a depth of millions of sequences per sample.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22402401">Ultra-high-throughput microbial community analysis on the Illumina HiSeq and MiSeq platforms.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23202435">Quality-filtering vastly improves diversity estimates from Illumina amplicon sequencing.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699611">Human gut microbiome viewed across age and geography.</a></li> </ul>' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name},
    'ANOTHER_COPY_RESULTS_ANS': 'You can download a copy from our website. Log in with your account name and password, go to the left side bar, move your mouse to Human Samples -> PARTICIPANT NAME -> SAMPLE NUMBER, and then click on SAMPLE NUMBER.pdf to download it.' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name},
    'FIND_DETAILED_INFO_ANS': 'You can find the raw data from European Bioinformatics Institute (please see <a href="#faq8">here</a>) or download the copy of your result from our website (please see <a href="#faq20">here</a>).',
    'WHEN_RESULTS_NON_FECAL': 'I sent in a non-fecal sample and have not received any results, when should I expect results?',
    'WHAT_FORMS': 'What are the forms you talk about on the sampling instructions?',
    'INTRODUCTION_TEXT': '<h4>What is a Gut?</h4> <p>Your gut is a hole that runs through your body. Your gut is actually, developmentally speaking, the outside of your body, but it has evolved many intricacies that make it seem like the inside. Your gut starts with your mouth and ends with your anus. In between food is changed into energy, feces, bacteria, viruses and a few other things. Your gut exacts a kind of metamorphosis on everything you eat, turning hotdog or grilled cheese, miraculously, into energy and, ultimately, cells, signals and even thoughts. We are only beginning to understand this process, a process in which microbes play (or fail to play) a major role.</p>'
                                '      <h4>What is %(shorthand)s?</h4>      <p>%(shorthand)s is a project in which scientists aim to work with non-scientists both to help them (AKA, you) understand the life inside their own guts and to do science. Science is coolest when it is informs our daily lives and what could possibly be more daily than what goes on in your gut? One of the big questions the %(shorthand)s scientists hope to figure out is what characterizes healthy and sick guts (or even just healthier and sicker guts) and how one might move from the latter to the former. Such is the sort of big lofty goal these scientists dream about at night (spirochetes rather than sugarplums dancing through their heads), but even the more ordinary goals are exciting. Even just beginning to know how many and which species live in our guts will be exciting, particularly since most of these species have never been studied, which is to say there are almost certainly new species inside you, though until you sample yourself (and all the steps that it takes to look at a sample happen&mdash; the robots, the swirling, the head scratching, the organizing of massive datasets), we won\'t know which ones. Not many people get to go to the rainforest to search for, much less discover, a new kind of monkey, but a new kind of bacteria, well, it is within (your toilet paper\'s) reach.</p>'
                                '      <h4>What is 16S rRNA?</h4>      <p>16S rRNA is a sort of telescope through which we see species that would otherwise be invisible. Let me explain. Historically, microbiologists studied bacteria and other microscopic species by figuring out what they ate and growing them, on petri dishes, in labs, in huge piles and stacks. On the basis of this approach&mdash; which required great skill and patience&mdash; thousands, perhaps hundreds of thousands, of studies were done. But then&hellip; in the 1960s, biologists including the wonderful radical <a href="http://www.robrdunn.com/2012/12/chapter-8-grafting-the-tree-of-life/">Carl Woese</a>, began to wonder if the RNA and DNA of microbes could be used to study features of their biology. The work of Woese and others led to the study of the evolutionary biology of microbes but it also eventually led to the realization that most of the microbes around us were not culturable&mdash; we didn\'t know what they ate or what conditions they needed. This situation persists. No one knows how to grow the vast majority of kinds of organisms living on your body and so the only way to even know they are there is to look at their RNA. There are many bits of RNA and DNA that one might look at, but a bit called 16S has proven particularly useful.</p>'
                                '      <h4>Do you really have a robot?</h4>      <p>Look, here is the deal. Robots. Microbiologists use robots. Personally, I think the fact that microbiologists study the dominant fraction of life on Earth, a fraction that carries out most of the important process (and a fair bit of inexplicable magic) makes microbiologists cool. I am not a microbiologist; I am an evolutionary biologist and a writer, but I think that microbiologists are hipsters cloaked in scientists clothing (and language). But if the outrageousness of their quarry does not convince you they are hip, well, then, let me remind you, they have robots.<br/>&nbsp;<br/>The robots enable the scientists to rapidly extract the DNA and RNA from thousands of samples simultaneously. Specifically, they can load your samples into small plastic plates each with 96 little wells. The robot then loads chemicals into the wells and heats the chemically-laced wells enough to break open the bacterial cells in the sample, BAM! This releases the cell\'s DNA and RNA. The robots then decode the specific letters (nucleotides) of the 16S gene using the nucleotides dumped out of the broken microbial cells into these plates.      <h4>Tree of life</h4>      <p>There is an evolutionary tree inside you. Well, sort of. When scientists study the microbes in your gut (and from the same samples we could also study viruses, bacteriophages&mdash; the viruses that attack bacteria&mdash;, fungi or even the presence of animals such as worms of various sorts) they do so by looking at the 16s or other genetic code of the RNA on the swabs you send us. We compare the code of each bit of RNA we find to the code of species other people have collected and also the code of the other bits of RNA in your sample. As a result, we can actually use the results of your sample to map the species living in you onto an evolutionary tree. Your own genes occupy one tiny branch on the tree of life, but the species inside of you come from all over the evolutionary tree. In fact, in some people we find species from each of the major branches of the tree of life (archaea, bacteria, eukaryotes) and then also many of the smaller branches. Inside you, in other words, are the consequences of many different and ancient evolutionary stories.</p>'
                                '      </p>'
                                '      <h4>What is a microbiome?</h4>      <p>A biome, as ecologists and evolutionary biologists like me historically used it is a self-contained ecosystem, where all the organisms can interact with each other and the environment in which they live, for example a rain forest is a biome, but it is made of smaller biomes, for example a tree is a biome for insects, then a single insect is a biome for bacteria. Therefore, these smaller biomes are often called microbiomes, in the case of you, it\'s your gut!&hellip; A microbiome is a small (micro) version of this larger phenomenon, a whole world within you.</p>'
                                '      <h4>What do my microbes eat?</h4>      <p>Everyplace you have ever set your hand or any other part of your body is covered in microbes. This is true of your gut, but also everything else. Microbes live in clouds. They live in ice. They live deep in the Earth. They also live in your colon, on your skin, and so on. It is reasonable to wonder what they eat. The short answer is everything. Microbes are thousands of times more variable when it comes to their diets than are animals, plants or even fungi. Some microbes can get their nitrogen out of the air; they can, in other words, eat air. Ain\'t that cool. Others, like us, eat other species, munching them in the world\'s coolest and most ubiquitous game of packman. The bacteria in your gut are also diverse in terms of their diets. If there are two hundred species of bacteria in your gut (and there probably are at least that many) then there are at least that many different combinations of things that they are eating.</p>'
                                '      <h4>Where do my microbes come from?</h4>      <p>If you had asked this question a few years ago, we would have had to say the stork. But increasingly we are beginning to understand more about where the specific zoo of species in you come from and it is a little grosser than the stork. If you were born vaginally, some of your gut microbes came from your mother\'s feces (birth, my friend, is messy). Some came from her vagina. Others came, if you were breast fed, from her milk. It is easiest for bacteria, it seems, to colonize our guts in the first moments of life. As we age, our stomachs become acidic. We tend to think of the acid of our stomachs as aiding in digestion; it does that but another key role of our stomachs is to prevent pathogenic species from getting into our guts. The trouble with this, well, there are a couple of problems. One is c-section birth. During c-section birth, microbes need to come from somewhere other than the mother\'s vagina and feces. The most readily available microbes tend to be those in the hospital. As a result, the microbes in c-section babies tend to, at least initially, resemble those of the hospital more than they resemble those of other babies. With time, many c-section babies eventually get colonized by enough good bacteria (from pet dogs, pet cats, their parents\' dirty hands, etc..) to get good microbes, but it is a more chancy process. But then, the big question, one we just don\'t know the answer to, is which and how many microbes colonize our guts as we get older. How many microbes ride through the acid bath of our stomach on our food and take up residence? We know that bad bacteria, pathogens, do this, but just how often and how good ones do it is not well worked out. You might be thinking, what about yoghurt and I\'ll tell you the answer, definitely, is we don\'t really know. Do people who eat yoghurt have guts colonized by species from that yoghurt? Maybe, possibly, I bet they do, but we don\'t really know (though if we get enough samples from yoghurt and non yoghurt eaters, we could know).</p>'
                                '      <h4>What will we discover in your gut?</h4>      <p>When the early meetings were going on about this project, everyone sat around talking about what we might see from colon samples. One scientist was sure that we would see bacteria that looked like Elvis. Another though we would find Shakespeare\'s great lost play. But the truth is all that we are going to see from your gut are lists of nucleotides. Let me explain&hellip;<br/>&nbsp;<br/>Nucleotides are those hunks of protein out of which DNA and RNA are made. They come in different forms to which scientists have assigned names and letters. When the robots are done with the work, what they produce are lists of the nucleotides in all of 16S genes from all of the cells in your sample. These nucleotides tell the scientists which kinds of life are in your sample (and in you). But because we will only have samples of little stretches of the 16S genes, we won\'t know exactly which species are in you, just which lineages they are from. You might have the bacterial equivalent of a chimpanzee and a gorilla in you, but all we\'ll know from your sample is that there was an ape. Knowing you have a bacterial ape in your gut will, on its own, not tell you so much. The real information will come from context, statistical context. I know, that sounds boring, but I promise it is not.<br/>&nbsp;<br/>We think that hundreds of different things you do during your life, in addition to what your mother and father did (let\'s try not to think about that), your genes and even just where you grew up influence which species of microbes are found inside you. But we don\'t really know. The problem is humans are so darn complicated. What we need to be able to do is to compare large numbers of people, people who differ in many ways, to be able to sort out which variables are sometimes a little important and which ones are the big deal. Is a vegan gut very different from a vegetarian one? Does eating yoghurt make a big difference? Do the effects of a c-section birth last forever? These questions require us to compare many people, which is where you come in. Your sample, gives us context and it gives you context too. It won\'t be terribly exciting on its own (you will know which ancient lineages you have dividing and thriving inside you. OK, that is pretty cool on second thought), but it will be very exciting in context. Where do you fall relative to fish eaters, sick people healthy people, hunter gatherers, or even your dog? You will know and we will know. And this is not all.<br/>&nbsp;<br/>All of the questions I have mentioned so far are what I might call first order questions. How does this thing compare to that thing. But what we\'d love to be able to answer are second order questions, contingent questions, questions such as whether the effect of your diet depends on your ethnicity (it probably does), whether the effect of having a dog depends on whether or not you live in the city (again, I bet it does) and so on. These questions are exactly the sort of question we have failed to be able to answer well when it comes to diet, because we don\'t have big enough samples sizes. We can see the forest for all of humans. Well, that isn\'t quite right, but you get the idea, we will be able to understand elaborate effects of multiple variables on the wilderness between your pie hole and the other hole and that, to us, is exciting.</p>'
                                '<h4>A few of the stories of the evolutionary tree in your gut</h4><p>Some people have least favorite bacteria. Salmonella, for example, seems to have inspired some haters. But microbiologists also have favorite bacteria, as well they should. The stories of bacteria (and those who chase and study them) are among the most important of humanities stories and include the tales of many species without which we could not live, or whose presence or absence affects how we live. These species are as fascinating and, dare I say, lovely as pandas or koala bears, just harder to see and far more significant. I have begun to compile a book of the stories of some of the most common and interesting species you are likely to encounter&mdash; whether in your own gut, on your lettuce or the next time you sink your fingers into the soil. These stories will be available online here at <a href="http://invisiblelife.yourwildlife.org/">Invisible Life</a> as they are compiled as a book, a book written by some of the very best science writers AND scientists out there. For starters, you might be interested to know that <a href="http://invisiblelife.yourwildlife.org/mycoplasma/">the smallest species on Earth</a> is sometimes found inside humans and, once we look at your 16S, we will even know whether it lives in you. As more of these stories are written, they will appear here, eventually as an ebook, an ebook that you can reference when you find out what lives inside you to know whether your constant companion is a species we know everything about or, as is more typical, no one has ever studied. Like Charlie Chaplin once said&hellip; Wait, Charlie Chaplin was the one who didn\'t say anything wasn\'t he.</p>' % {"shorthand": AMGUT_CONFIG.project_shorthand, "project": AMGUT_CONFIG.project_name},
    'ANOTHER_COPY_RESULTS': 'Can I get another copy of my results?',
    'NOT_A_BUSINESS': 'We are not a business',
    'WHERE_SEND_SAMPLE_ANS': '<p>This is the shipping address:</p>'
                                'American Gut Project<br>Knight Lab, JSCBB<br>596 UCB<br>Boulder, CO 80309<p>If you are shipping internationally, please see the <a href="/international_shipping/">international shipping instructions</a>.'
}


_TAXA_SUMMARY = {'RESOLUTION_NOTE': "Note: Where there are blanks in the table below, the taxonomy could not be resolved in finer detail.",
                 'PERCENTAGES_NOTE': "Note: The percentages listed represent the relative abundance of each taxon. This summary is based off of normalized data. Because of limitations in the way the samples are processed, we cannot reliably obtain species level resolution. As such, the data shown are collapsed at the genus level.",
                 'DOWNLOAD_LINK': "Download the table"}


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
    'MESSAGE': 'Please help us to debug by emailing us at <a href="mailto:%(help_email)s">%(help_email)s</a> and tell us exactly what happend before you got this error.',
    'SIGNOFF': 'Thanks, <br /> The American Gut Team'
}

_404 = {
    'MAIN_WARNING': '404: Page not found!',
    'HELP_TEXT': 'Click <a href="mailto:%(help_email)s">HERE</a> to email us about the issue. Please include the URL you were trying to access:' % {'help_email': media_locale['HELP_EMAIL']}
}

_PARTICIPANT_OVERVIEW = {
    'COMPLETED_CONSENT': 'Completed consent',
    'COMPLETED_SURVEY': 'Completed survey',
    'SAMPLES_ASSIGNED': 'Samples assigned',
    'OVERVIEW_FOR_PARTICPANT': 'Overview for participant'
}

_ADD_SAMPLE_OVERIVIEW = {
    'ADD_SAMPLE_TITLE': 'Choose your sample source ',
    'ADD_SAMPLE_TITLE_HELP': 'The sample source is the person, animal or environment that the sample you are currently logging came from. If you took the sample from yourself, you should select yourself as the sample source.',
    'ENVIRONMENTAL': 'Environmental',
    'ADD_SAMPLE_1': 'If you don\'t see the sample source you want here, you need to add it. You can do this in ',
    'ADD_SAMPLE_2': 'Step 2',
    'ADD_SAMPLE_3': ' on the main page when you log in.',
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

_CHANGE_PASS_VERIFY = {
    'ENTER_PASS': 'Please enter new password',
    'NEW_PASS': 'New Password:',
    'NEW_PASS_TITLE': 'The new password you would like to use to log in from now on.',
    'CONFIRM_PASS': 'Confirm Password:',
    'CONFIRM_PASS_TITLE': "Repeat your New Password again, exactly as before. We ask you to repeat it here so that you don't accidentally change your password to something you did not intend.",
    'INVALID': "Your password change code is not valid. If you wish to change your password please <a href='/forgot_password/'>start over</a>",
    'CHANGED': 'Your password has been changed',
    'NO_EMAIL': "<h2> Could not send Email </h2><p> We attempted to email the message below: <p><p>This is a courtesy email to confirm that you have changed your password for your kit with ID  {{kitid}} If you did not request this change, please email us immediately at info@americangut.org.' <p>",
    'CHANGE_PASS': 'Change password'
}

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
    'EMAIL_EXCEPTION': 'There was a problem sending you the kit ID. Please contact us directly at <a href="%(help_email)s">%(help_email)s</a>.' % {'help_email': media_locale['HELP_EMAIL']},
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
    '404.html': _404,
    'FAQ.html': _FAQ,
    'db_error.html': _DB_ERROR,
    'retrieve_kitid.html': _RETREIVE_KITID,
    'add_sample.html': _ADD_SAMPLE,
    'error.html': _ERROR,
    'forgot_password.html': _FORGOT_PASSWORD,
    'change_pass_verify.html': _CHANGE_PASS_VERIFY,
    'help_request.html': _HELP_REQUEST,
    'add_sample_overview.html': _ADD_SAMPLE_OVERIVIEW,
    'participant_overview.html': _PARTICIPANT_OVERVIEW,
    'sample_overview.html': _SAMPLE_OVERVIEW,
    'taxa_summary.html': _TAXA_SUMMARY,
    'construction.html': _CONSTRUCTION,
    'register_user.html': _REGISTER_USER
    }
