#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from amgut.lib.config_manager import AMGUT_CONFIG
from amgut.lib.locale_data import english_gut as ENG

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The American Gut Project Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

# Any media specific localizations
_SITEBASE = AMGUT_CONFIG.sitebase

media_locale = {
    'ANALYTICS_ID': 'UA-55355651-1',
    'FUNDRAZR_URL': "https://fundrazr.com/campaigns/4sSf3",
    'KIT_INSTRUCTIONS': _SITEBASE + '/static/img/bg_kit_instructions.pdf',
    'LATITUDE': 54.5,
    'LOGO': _SITEBASE + '/static/img/bg_logo.png',
    'LONGITUDE': -3.5,
    'SHIPPING_ADDRESS': 'Gabriela Surdulescu<br/>Department of Twin Research<br/>St. Thomas’ Hospital Campus<br>The Rayne Institute, Lambeth Wing, 4th Floor<br/>Westminster Bridge Road, London SE1 7EH',
    'ZOOM': 6
}
media_locale.update(ENG.media_locale)

_HANDLERS = ENG._HANDLERS

_NEW_PARTICIPANT = {
    'CONSENT_18':
        '''<p align='center'><b>University of California, San Diego</b><br/>
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
<li>All in the Family - Where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shallow shotgun metagenomic analysis") of up to four faecal samples with analysis of the pathways used by bacteria to signal other bacteria or within themselves;</li>
<li>Beyond Bacteria - Deeper shotgun metagenome and virome characterisation (where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present making use of additional gene parts that can tell us if there are any associated viruses or virus products that "talk " with bacteria, fungus and parasites that may be present in the sample from your gut.  Requires shipment of a whole stool sample (materials and return FedEx postage included) ($2500/kit);</li>
<li>Functional Feces - Additional characterisation of gut samples over time (up to 7 stool samples, providing an analysis of the variability of functions over time. Here too the DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shotgun metagenomic analysis").</li>
</ol>
<p>We will analyse all samples where the consent form and questionnaire is completed.  The samples in the project (including yours) will be analysed and published as a scientific article defining the range of diversity in the human microbiome.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to a more detailed list of the different organisms present in your sample (taxonomy summary).</p>
<p>We would like you to understand from the consent what we will do with your sample and what you will get in return.</p>

<p>We will ask you to complete an online questionnaire about you your lifestyle and what you eat.  We estimate that this should take no more than 30 minutes. You will then sample a part of your body (of interest to you) with a sterile Q-tip like swab by rubbing the surface of your skin, rubbing the surface of your tongue or sampling your stool by inserting the tip of the swab into used toilet tissue.  You can also sample other parts of your body - ear, nose, vagina, scalp, sole of foot. The swabs should be returned to us in the envelope provided using regular US mail service. DNA will be extracted from the sample and amplified by PCR (polymerase chain reaction) and then sequenced to see what bacteria are present and in what proportion in your sample. We estimate that it will take 2 months for you to learn the results.</p>
<p>For the Beyond Bacteria package you will submit a whole stool sample in a designated collection device on special ice packs (that reliably cool the sample to -20 degrees celsius/-4 degrees Fahrenheit) in a container that we will provide.  The results for "Beyond Bacteria" and "All in the family" will take longer to analyse because more extensive analysis is provided.  Results will be uploaded to your American Gut account when they are available.  We are also asking you to consent to having your sample or the bacterial DNA from it to be used in future studies.</p>

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

<p>We will analyse all samples where the consent form and questionnaire is completed.  The samples in the project (including yours) will be analysed and published as a scientific article.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed taxa report of your results.</p>
<p>The results from analysis of your sample/s cannot be used by you or your doctor to confirm a clinical diagnosis and we are not testing for infectious disease.</p>

<p style='font-weight: bold;'>Can you choose to not participate or withdraw from the study without penalty or loss of benefits?</p>
<p>Participation in research is entirely voluntary. You may refuse to participate or withdraw at any time without penalty or loss of benefits to which you are entitled. If you decide that you no longer wish to continue in this study, you will be requested to contact the American Gut Project helpline to inform us of your intent to withdraw.  If your sample has not been processed you may request a refund which will be processed through the site where you contributed to the project.</p>
<p>You will be told if any important new information is found during the course of this study that may affect your wanting to continue.</p>

<p style='font-weight: bold;'>Can you be withdrawn from the study without your consent?</p>
<p>You may be withdrawn from the study if you do not complete the consent. You may also be withdrawn from the study if you do not follow the instructions given you by the study personnel.</p>

<p style='font-weight: bold;'>Will you be compensated for participating in this study?</p>
<p>You will not be financially compensated in this study.</p>

<p style='font-weight: bold;'>Are there any costs associated with participating in this study?</p>
<p>You will be asked to contribute money to the project commensurate with the investigation you request ($99 for one sample, $1500 for "All in the family" (shallow shotgun metagenomic sequencing) and $2500 for "Beyond Bacteria" (deeper shotgun metagenome and virome characterisation of one sample, plus additional sequencing). A receipt will be sent to you after you pay for the analysis you are requesting.  These contributions are used to partially finance the project.  Any additional funds required are provided from the funds UCSD has provided to Dr. Knight to set up his laboratory.</p>

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
    'CONSENT_YOUR_CHILD': '''<p align='center'><b>University of California, San Diego</b><br/>
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
<li>All in the Family - Where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shallow shotgun metagenomic analysis") of up to four faecal samples with analysis of the pathways used by bacteria to signal other bacteria or within themselves;</li>
<li>Beyond Bacteria - Deeper shotgun metagenome and virome characterisation (where bacterial DNA is sliced up into fragments and then reassembled to see what genes are present making use of additional gene parts that can tell us if there are any associated viruses or virus products that "talk " with bacteria, fungus and parasites that may be present in the sample from your gut.  Requires shipment of a whole stool sample (materials and return FedEx postage included) ($2500/kit);</li>
<li>Functional Feces - Additional characterisation of gut samples over time (up to 7 stool samples, providing an analysis of the variability of functions over time. Here too the DNA is sliced up into fragments and then reassembled to see what genes are present (also called "shotgun metagenomic analysis").</li>
</ol>
<p>We will analyse all samples where the consent form and questionnaire is completed.  The samples in the project (including your child's) will be analysed and published as a scientific article defining the range of diversity in the human microbiome.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed list of the different organisms present in your sample (taxonomy summary).</p>
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

<p style='font-weight: bold;'>We will analyse all samples where the consent form and questionnaire is completed.  The samples in the project (including your child's) will be analysed and published as a scientific article.  You will get a link to view, download and print a high-resolution certificate suitable for framing of your results and access to more detailed taxa report of your results.</p>
<p>The results from analysis of your sample/s cannot be used by you or your doctor to confirm a clinical diagnosis and we are not testing for infectious disease.</p>

<p style='font-weight: bold;'>Can your child be withdrawn from the study without your consent?</p>
<p>Participation in research is entirely voluntary. You may refuse to participate or withdraw your child from the study at any time, without penalty or loss of benefits to which you are entitled. If you decide that you no longer wish to continue in this study, you will be requested to contact the American Gut Project helpline to inform us of your intent to withdraw.  If your sample has not been processed you may request a refund which will be processed through the site where you contributed to the project.</p>
<p>You will be told if any important new information is found during the course of this study that may affect your wanting to continue.</p>

<p style='font-weight: bold;'>Will you be compensated for participating in this study?</p>
<p>You will not be financially compensated in this study.</p>

<p style='font-weight: bold;'>Are there any costs associated with participating in this study?</p>
<p>You will be asked to contribute money to the project commensurate with the investigation you request ($99 for one sample, $1500 for "All in the family" (shallow shotgun metagenomic sequencing) and $2500 for "Beyond Bacteria" (deeper shotgun metagenome and virome characterisation of one sample, plus additional sequencing). A receipt will be sent to you after you pay for the analysis you are requesting.  These contributions are used to partially finance the project.  Any additional funds required are provided from the funds UCSD has provided to Dr. Knight to set up his laboratory.</p>

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
<li><b>Non-Interference.</b> Notwithstanding any other provision contained herein, the use of UCSD facilities and/or UCSD personnel in support of this Agreement can only be authorised to the extent that it will not interfere with work related to the prime missions of UCSD and/or the Department (e.g., education and research).  Accordingly, Individual's exclusive remedy for failure by either UCSD or persons acting on its behalf to perform services or furnish information or data hereunder at any particular time or in any specific manner, is limited to reimbursement of any unexpended payments under this Agreement.</li>
<li><b>Non-Exclusive Nature of Services.</b>  The Services herein are being offered to Individual on a non-exclusive basis.  Nothing herein shall be construed as granting Company any exclusive right(s) to the Service(s) referenced herein, and UCSD retains the right to offer and perform similar or identical Services for others.</li>
<li><b>Notice.</b>  Any notice or communication required by this Agreement shall be in writing and shall be deemed to have been duly given if delivered personally, or sent by overnight mail, or prepaid registered mail, email, or confirmed facsimile transmission, addressed to the other party at the address set forth on kit registration, or at such other address as such party hereto may hereafter specify in writing to the other party.</li>
<li><b>Status of Parties.</b>  This Agreement is not intended to create, nor shall it be construed to be, a joint venture, association, partnership, franchise, or other form of business relationship.  Neither party shall have, nor hold itself out as having, any right, power or authority to assume, create, or incur any expenses, liability, or obligation on behalf of the other party, except as expressly provided herein.</li>
<li><b>Third-Party Beneficiary.</b>  There are no intended third-party beneficiaries to this Agreement.</li>
<li><b>Severability.</b>  If any provision of this Agreement is held invalid, illegal or unenforceable in any respect, such provision shall be treated as severable, leaving the remaining provisions unimpaired, provided that such does not materially prejudice either party in their respective rights and obligations contained in the valid terms, covenants, or conditions.</li>
<li><b>Non-Waiver.</b>  The failure of either party to require the performance of any of the terms of this Agreement or the waiver by either party of any default under this Agreement shall not prevent a subsequent enforcement of such term, nor be deemed a waiver of any subsequent breach.</li>
<li><b>Modification of Agreement.</b>  This Agreement shall be changed only by written agreement of the parties.</li>
<li><b>Applicable Law.</b>  This Agreement shall be governed by the laws of the State of California without regard to its conflict of laws provisions.</li>
<li><b>Signatures, Counterparts and Copies.</b>  This Agreement may be executed in counterparts, all of which, when taken together, shall constitute one contract with the same force and effect as if all signatures had been entered on one document.  Signatures may be made electronically, by clicking "I Agree" and such electronic signatures shall be valid and binding upon the parties making them, and shall serve in all respects as original signatures. Upon clicking "I Agree" this agreement shall be considered fully-executed by both parties. Signatures may be delivered among and between the parties by facsimile or electronic means.  Thereafter, the parties further agree that electronic copies of this Agreement may be used for any and all purposes for which the original may have been used.</li>
<li><b>Arbitration.</b>  In the event of any dispute, claim, question, or disagreement arising from or relating to this Agreement or the breach thereof, the parties hereto shall use their best efforts to settle the dispute, claim, question, or disagreement.  To this effect, they shall consult and negotiate with each other in good faith and recognising their mutual interests, attempt to reach a just and equitable solution satisfactory to both parties.  If they do not reach a solution within a period of sixty (60) days, then upon notice by either party to the other, all disputes, claims, questions, or disagreements shall be finally settled in accordance with the provisions of the American Arbitration Association ("AAA") and proceed under the provisions of Title 9 of the California Code of Civil Procedure Sections 1280 through and including 1294.2.  The discovery provisions of the California Code of Civil Procedure Section 1283.05 shall be applicable to this Agreement.  Each party shall bear its own costs.</li>
<li><b>Export Control.</b>  No ITAR or export controlled materials shall be delivered to UCSD pursuant to this agreement.   </li>
<li><b>Entire Agreement.</b>  This Agreement, including Exhibit A made a part hereof, sets forth the entire agreement of the parties with respect to the subject matter herein and supersedes any prior agreements, oral and written, and all other communications between the parties with respect to such subject matter.</li>
</ol><br/>''',
}
_NEW_PARTICIPANT.update(ENG._NEW_PARTICIPANT)

_FAQ = {
    'HOW_PROCESS_SAMPLES_ANS_6': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21552244">Minimum information about a marker gene sequence (MIMARKS) and minimum information about any (x) sequence (MIxS) specifications.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24280061">EMPeror: a tool for visualising high-throughput microbial community data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16332807">UniFrac: a new phylogenetic method for comparing microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/16893466">UniFrac--an online tool for comparing microbial community diversity in a phylogenetic context.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17220268">Quantitative and qualitative beta diversity measures lead to different insights into factors that structure microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/19710709">Fast UniFrac: facilitating high-throughput phylogenetic analyses of microbial communities including analysis of pyrosequencing and PhyloChip data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20827291">UniFrac: an effective distance metric for microbial community comparison.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21885731">Linking long-term dietary patterns with gut microbial enterotypes.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23326225">A guide to enterotypes across the human body: meta-analysis of microbial community structures in human microbiome datasets.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699609">Structure, function and diversity of the healthy human microbiome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699610">A framework for human microbiome research.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23587224">The Biological Observation Matrix (BIOM) format or: how I learned to stop worrying and love the ome-ome.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22134646">An improved Greengenes taxonomy with explicit ranks for ecological and evolutionary analyses of bacteria and archaea.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304728">The Earth Microbiome Project: Meeting report of the "1 EMP meeting on sample selection and acquisition" at Argonne National Laboratory October 6 2010.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21304727">Meeting report: the terabase metagenomics workshop and the vision of an Earth microbiome project.</a></li> </ul>' % {'project_name': AMGUT_CONFIG.project_name},
    'HOW_PROCESS_SAMPLES_ANS_10': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/17881377">Short pyrosequencing reads suffice for accurate microbial community analysis.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18723574">Accurate taxonomy assignments from 16S rRNA sequences produced by highly parallel pyrosequencers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/18264105">Error-correcting barcoded primers for pyrosequencing hundreds of samples in multiplex.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22237546">Selection of primers for optimal taxonomic classification of environmental 16S rRNA gene sequences.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22170427">Comparison of Illumina paired-end and single-direction sequencing for microbial 16S rRNA gene amplicon surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21716311">Impact of training sets on classification of high-throughput bacterial 16s rRNA gene surveys.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/21349862">PrimerProspector: de novo design and taxonomic analysis of barcoded polymerase chain reaction primers.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20383131">QIIME allows analysis of high-throughput community sequencing data.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22161565">Using QIIME to analyse 16S rRNA gene sequences from microbial communities.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23861384">Meta-analyses of studies of the human microbiota.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/24060131">Advancing our understanding of the human microbiome using QIIME.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20534432">Global patterns of 16S rRNA diversity at a depth of millions of sequences per sample.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22402401">Ultra-high-throughput microbial community analysis on the Illumina HiSeq and MiSeq platforms.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/23202435">Quality-filtering vastly improves diversity estimates from Illumina amplicon sequencing.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/22699611">Human gut microbiome viewed across age and geography.</a></li> </ul>',
    'HOW_PROCESS_SAMPLES_ANS_8': '<ul> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20412303">Effect of storage conditions on the assessment of bacterial community structure in soil and human-associated samples.</a></li> <li><a href="http://www.ncbi.nlm.nih.gov/pubmed/20673359">Sampling and pyrosequencing methods for characterising bacterial communities in the human gut using 16S sequence tags.</a></li> </ul>',
    'ONLY_FECAL_RESULTS': "I sent more than one kind of sample, but I only received data for my faecal sample. What happened to my other samples?",
<<<<<<< HEAD
    'ONLY_FECAL_RESULTS_ANS': 'Results are only available for faecal, oral, and skin samples. We are in the process of evaluating how best to present the other sample types. Please see <a href="#faq16">the previous question </a>',
    'PROJECT_RELATION': 'What is the British Gut’s relation to the American Gut?',
    'PROJECT_RELATION_ANS': "The British Gut is considered a “sister site” to the American Gut--so while it has a separate site of operations at <a href='http://www.twinsuk.ac.uk/'>King's College London</a> with TwinsUK, some of the operations tie back to the American Gut framework (examples include samples being processed at American Gut’s site at the University of California San Diego, emails being directed to the American Gut help account).<p>The British Gut was set up as a unique collaboration in order to be able to extend and collect samples from European participants.  By having a site set up in Europe, the time and cost for sending out kits, receiving samples, and sending samples back for analysis are greatly reduced.</p><p>Ultimately, both the American Gut and British Gut tie back to a larger umbrella known as <a href='http://microsetta.ucsd.edu'>The Microsetta Initiative</a>, which was an effort started in 2018 that wishes to collect microbiome samples and rich phenotypic data across the world’s populations.</p>",
    'RAW_DATA_ANS_2': 'Processed sequence data and open-access descriptions of the bioinformatic processing can be found at our <a href="https://github.com/qiime/American-Gut">Github repository</a>.</p>'
                      '<p>Sequencing of %(project_shorthand)s samples is an on-going project, as are the bioinformatic analyses. These resources will be updated as more information is added and as more open-access descriptions are finalised.' % {'project_shorthand': AMGUT_CONFIG.project_shorthand},
    'WHEN_RESULTS_NON_FECAL_ANS': "The vast majority of the samples we've received are faecal, which was why we prioritised those samples. Much of the analysis and results infrastructure we've put in place is applicable to other sample types, but we do still need to assess what specific representations of the data make the most sense to return to participants. We apologise for the delay.",
    'WHERE_SEND_SAMPLE_ANS': '<p>This is the shipping address:</p>%(shipping)s' % {'shipping': media_locale['SHIPPING_ADDRESS']}
}
_FAQ.update(ENG._FAQ)

_INTRODUCTION = {
    'INTRODUCTION_WHAT_IS_PROJECT': "<p>The %(project_name)s is a project in which scientists aim to work with non-scientists both to help them (AKA, you) understand the life inside their own guts and to do science. Science is coolest when it is informs our daily lives and what could possibly be more daily than what goes on in your gut? One of the big questions the %(project_shorthand)s scientists hope to figure out is what characterises healthy and sick guts (or even just healthier and sicker guts) and how one might move from the latter to the former. Such is the sort of big lofty goal these scientists dream about at night (spirochetes rather than sugarplums dancing through their heads), but even the more ordinary goals are exciting. Even just beginning to know how many and which species live in our guts will be exciting, particularly since most of these species have never been studied, which is to say there are almost certainly new species inside you, though until you sample yourself (and all the steps that it takes to look at a sample happen&mdash; the robots, the swirling, the head scratching, the organising of massive datasets), we won't know which ones. Not many people get to go to the rainforest to search for, much less discover, a new kind of monkey, but a new kind of bacteria, well, it is within (your toilet paper's) reach." % {'project_shorthand': AMGUT_CONFIG.project_shorthand, 'project_name': AMGUT_CONFIG.project_name},
    'INTRODUCTION_WHAT_IS_16S': "16S rRNA is a sort of telescope through which we see species that would otherwise be invisible. Let me explain. Historically, microbiologists studied bacteria and other microscopic species by figuring out what they ate and growing them, on petri dishes, in labs, in huge piles and stacks. On the basis of this approach&mdash; which required great skill and patience&mdash; thousands, perhaps hundreds of thousands, of studies were done. But then&hellip; in the 1960s, biologists including the wonderful radical <a href=\"http://www.robrdunn.com/2012/12/chapter-8-grafting-the-tree-of-life/\">Carl Woese</a>, began to wonder if the RNA and DNA of microbes could be used to study features of their biology. The work of Woese and others led to the study of the evolutionary biology of microbes but it also eventually led to the realisation that most of the microbes around us were not culturable&mdash; we didn't know what they ate or what conditions they needed. This situation persists. No one knows how to grow the vast majority of kinds of organisms living on your body and so the only way to even know they are there is to look at their RNA. There are many bits of RNA and DNA that one might look at, but a bit called 16S has proven particularly useful.",
    'INTRODUCTION_MICROBES_COME_FROM': "If you had asked this question a few years ago, we would have had to say the stork. But increasingly we are beginning to understand more about where the specific zoo of species in you come from and it is a little grosser than the stork. If you were born vaginally, some of your gut microbes came from your mother's feces (birth, my friend, is messy). Some came from her vagina. Others came, if you were breast fed, from her milk. It is easiest for bacteria, it seems, to colonise our guts in the first moments of life. As we age, our stomachs become acidic. We tend to think of the acid of our stomachs as aiding in digestion; it does that but another key role of our stomachs is to prevent pathogenic species from getting into our guts. The trouble with this, well, there are a couple of problems. One is c-section birth. During c-section birth, microbes need to come from somewhere other than the mother's vagina and feces. The most readily available microbes tend to be those in the hospital. As a result, the microbes in c-section babies tend to, at least initially, resemble those of the hospital more than they resemble those of other babies. With time, many c-section babies eventually get colonised by enough good bacteria (from pet dogs, pet cats, their parents' dirty hands, etc..) to get good microbes, but it is a more chancy process. But then, the big question, one we just don't know the answer to, is which and how many microbes colonise our guts as we get older. How many microbes ride through the acid bath of our stomach on our food and take up residence? We know that bad bacteria, pathogens, do this, but just how often and how good ones do it is not well worked out. You might be thinking, what about yoghurt and I'll tell you the answer, definitely, is we don't really know. Do people who eat yoghurt have guts colonised by species from that yoghurt? Maybe, possibly, I bet they do, but we don't really know (though if we get enough samples from yoghurt and non yoghurt eaters, we could know)."
}
_INTRODUCTION.update(ENG._INTRODUCTION)

_TAXA_SUMMARY = {
    'PERCENTAGES_NOTE': "Note: The percentages listed represent the relative abundance of each taxon. This summary is based off of normalised data. Because of limitations in the way the samples are processed, we cannot reliably obtain species level resolution. As such, the data shown are collapsed at the genus level."
}
_TAXA_SUMMARY.update(ENG._TAXA_SUMMARY)

_BASIC_REPORT = ENG._BASIC_REPORT
_INTERACTIVE_REPORT = ENG._INTERACTIVE_REPORT
_HELP_REQUEST = ENG._HELP_REQUEST
_DB_ERROR = ENG._DB_ERROR
_404 = ENG._404

_403 = {
    'MAIN_WARNING': '403: Unauthorised access!'
}
_403.update(ENG._403)

_PARTICIPANT_OVERVIEW = ENG._PARTICIPANT_OVERVIEW
_ADD_SAMPLE_OVERVIEW = ENG._ADD_SAMPLE_OVERVIEW

_SAMPLE_OVERVIEW = {
    'DATA_VIS_TITLE': "Data Visualisation",
    'RESULTS_PDF_LINK': "Click this link to visualise sample %(barcode)s in the context of other microbiomes!",
}
_SAMPLE_OVERVIEW.update(ENG._SAMPLE_OVERVIEW)

_NEW_PARTICIPANT_OVERVIEW = {
    'ELECTRONIC_SIGNATURE': 'In order to participate in this study, you will need to sign a research consent form. This must be done electronically. To consent to using an electronic signature, please click the button below. To obtain a hard copy of the signed agreement, please email the help desk (britishgut@gmail.com). You may revoke this consent at any time by going to human samples -> person name -> remove person name. Revoking consent will also halt processing of your sample, if applicable. Once your sample is processed, we cannot remove it from the deidentified information distributed, regardless of consent revocation.'
}
_NEW_PARTICIPANT_OVERVIEW.update(ENG._NEW_PARTICIPANT_OVERVIEW)

_MAP = ENG._MAP
_FORGOT_PASSWORD = ENG._FORGOT_PASSWORD
_ERROR = ENG._ERROR
_RETREIVE_KITID = ENG._RETREIVE_KITID
_ADD_SAMPLE = ENG._ADD_SAMPLE

_REGISTER_USER = {
    'ENTER_ZIP': "Please enter your postcode",
    'REQUIRED_ZIP': 'Your postcode must be 10 or fewer characters',
    'ZIP': "Postcode"
}
_REGISTER_USER.update(ENG._REGISTER_USER)

_ADDENDUM = {
    'AG_POPULATION_ALT': "PCoA of American Gut population coloured by Firmicutes",
    'AG_POPULATION_TEXT': "This plot lets you compare your sample to other faecal microbiome samples we collected from American Gut participants. The colour indicates the relative abundance of Firmicutes bacteria each sample had with red being the lowest and purple being the highest. If you had a lot of Firmicutes bacteria, then your sample should be purple, and you can look for other purple samples to see how similar your whole bacterial community is to other people with high amounts of Firmicutes. As in the other plots, the location of the point along the axes means nothing. Only its relative position compared to the other points is meaningful.",
    'DIFFERENT_AGES_POPS_ALT': "PCoA of international populations coloured by age",
    'DIFFERENT_AGES_POPS_TEXT': "This plot lets you compare your sample to other faecal microbiome samples according to age and place of origin. The colour of each point indicates the age of the person the sample was collected from, with red being the youngest and purple being the oldest. Also, on this plot, the ovals show where in the world each sample came from. The red oval shows you the area where an average sample from a Western country should fall. The yellow oval shows you where an average sample from an Amerindian population in Venezuela should fall. The blue oval shows you where an average sample from Malawi should fall. These data are from <a href = 'http://www.nature.com/nature/journal/v486/n7402/abs/nature11053.html'>Yatsunenko et al. 2012</a>. We used these populations as a comparison to your sample since a large number of people with diverse ages were sampled in these populations. We have fewer data from other populations in other parts of the world.",
    'DIFFERENT_BODY_SITES_TEXT': "This plot lets you compare your sample to samples collected in other microbiome projects from several body sites. The colour of each point tells you which project and body site the sample came from. HMP refers to the <a href = 'http://www.hmpdacc.org'>Human Microbiome Project</a>, funded by the National Institutes of Health. You can see how your sample compared to faecal, oral, and skin samples from the Human Microbiome Project, as well as to faecal, oral, and skin samples from the American Gut Project, the Global Gut Project, and the Personal Genome Project. These samples have been combined in any category not labeled \"HMP\". The oval around each group of points shows you where an average sample from each project and body site should fall on the plot. These sometimes make it easier to see the patterns all the clusters of points make.",
    'MAJOR_PHYLA_ACTINOBACTERIA_TEXT': "A phylum of Gram-positive bacteria both terrestrial and aquatic. They are mostly recognised as excellent decomposers of resilient organic compounds such as cellulose or chitin. Although some can be plant and animal pathogens, others are more known as producers of antibiotics (e.g. Streptomyces).  In their body form, many resemble fungi by forming mycelial-like filaments.",
    'MAJOR_PHYLA_BACTEROIDETES_TEXT': "A phylum of Gram-negative bacteria, rod-shaped, present in all sorts of environments such as soil, sediments, and fresh and marine waters. Most are saprophytic and involved in carbon cycling. Often abundant in nutrient-rich habitats and so they are a major component of animal guts where they can act as degraders of complex carbohydrates and proteins but also as pathogens. Their representatives are organised within 4 major classes among which the genus <em>Bacteroides</em> in the class of Bacteroidia is the most prevalent and the most studied. Bacteroidetes together with Firmicutes make up the majority of gut bacteria. The ratio of these two types of bacteria (specifically the dominance of Firmicutes over Bacteroidetes) may be linked to obesity.",
    'MAJOR_PHYLA_FIRMICUTES_TEXT': "A phylum of bacteria with generally Gram-positive (retain crystal violet dye) staining cell wall structure. The names is derived from Latin <em>firmus</em> for strong and <em>cutis</em> for skin. The cells are in the form of spheres called cocci (singular coccus) or rods called bacilli (singular bacillus). Firmicutes encompass bacteria that can be found in many different environments ranging from soil to wine to your gut. There are currently more than 274 genera representing 7 different classes of which Clostridia (anaerobes - no oxygen) and Bacilli (obligate or facultative aerobes) are the most significant. Both classes are predominantly saprophytic (getting nourishment from dead or decaying organic matter) playing an important role in the decomposition and nutrient mineralisation processes, but also contain a few human pathogens (e.g. <em>Clostridium tetani</em> or <em>Bacillus anthracis</em>).",
    'MAJOR_PHYLA_PROTEOBACTERIA_TEXT': "A phylum of Gram-negative bacteria. They are named after a Greek God Proteus to illustrate their variety of forms. They are organised in 6 recognised classes and represent all types of metabolisms ranging from heterotrophic to photosynthetic to chemoautotrophic.  They include many well-known pathogens (e.g., <em>Escherichia</em>, <em>Helicobacter</em>, <em>Salmonella</em>, <em>Vibrio</em>) as well as free-living types that can fix nitrogen (convert nitrogen present in the atmosphere into ammonia, a form of nitrogen available for plants&apos; uptake).",
    'MAJOR_PHYLA_TENERICUTES_TEXT': "A phylum of Gram-negative bacteria without a cell wall (<em>tener</em> - soft, <em>cutis</em> - skin) which are organised in a single class. Nutritionally, they represent variable pathways ranging from aerobic and anaerobic fermenters to commensals to strict pathogens of vertebrates (e.g., fish, cattle, wildlife). Among the best studied are Mycoplasmas with a fried egg-like shape and <em>Mycoplasma pneumoniae</em> is one of the best known examples of human pathogens causing pneumonia, bronchitis, and other respiratory conditions.",
    'TAXONOMY_INTRO': "Taxonomy is a system scientists use to describe all life on the planet. Taxonomy is commonly referred to as an organism&apos;s scientific name. This name allows us to understand how closely related two organisms are to each other. There are seven major levels of taxonomy that go from less specific to more specific. The phylum level represents very broad range of organisms that have <strong>evolved over hundreds of millions of years</strong> whereas the species level represents only a small subset of them that are <strong>much more closely related</strong>. Typically, names at the genus and species levels are written in <em>italics</em> or are <u>underlined</u> (in our tables, they are <em>italicised</em>). For instance, here is the list of taxonomic levels and names for humans and chimpanzees:"
}

_PORTAL = {
    'DOMESTIC_TEXT_1': "Shipping within the UK should be around £2.90, but we recommend taking the sample to the post office to get the proper postage. Getting the postage right on the first try is important since samples that spend a long time in transit will likely not produce the highest quality results.",
    'DOMESTIC_TEXT_3': media_locale['SHIPPING_ADDRESS'],
    'RESULTS_READY_TEXT_1': "One or more of the samples you submitted have been sequenced, and the results are now available online! Currently, we have only processed faecal samples, but we will be processing samples from other body sites soon.",
    'RESULTS_TEXT_2': "Sequencing and data analysis can take up to 4 months, please be patient! We will let you know as soon as your samples have been sequenced and analysed. Once your results are ready, we will send you an email notification.",
    'SAMPLE_STEPS_TEXT_5': "For a <strong>faecal sample</strong>, rub both cotton tips on a faecal specimen (a used piece of bathroom tissue). Collect a small amount of biomass. Maximum collection would be to saturate 1/2 a swab. <strong>More is not better!</strong> The ideal amount of biomass collected is shown below."
}
_PORTAL.update(ENG._PORTAL)

_CHANGE_PASS_VERIFY = ENG._CHANGE_PASS_VERIFY
_SURVEY_MAIN = ENG._SURVEY_MAIN
_HUMAN_SURVEY_COMPLETED = ENG._HUMAN_SURVEY_COMPLETED

# helper tuples for the survey questions
_NO_RESPONSE_CHOICE = ENG._NO_RESPONSE_CHOICE
_YES_NO_CHOICES = ENG._YES_NO_CHOICES
_YES_NO_NOTSURE_CHOICES = ENG._YES_NO_NOTSURE_CHOICES
_FREQUENCY_MONTH_CHOICES = ENG._FREQUENCY_MONTH_CHOICES
_FREQUENCY_WEEK_CHOICES = ENG._FREQUENCY_WEEK_CHOICES
_DIAGNOSIS_CHOICE = ENG._DIAGNOSIS_CHOICE
_ANIMAL_SURVEY = ENG._ANIMAL_SURVEY

_PERSONAL_MICROBIOME = ENG._PERSONAL_MICROBIOME

_NOJS = {
    'MESSAGE': 'You have JavaScript disabled, which this site requires in order to function properly. <br/>Please enable javascript and reload <a href="http://www.microbio.me/britishgut">http://www.microbio.me/britishgut</a>.',
    'NEED_HELP': 'If you need help enabling JavaScript in your browser, <br/>Please email us at <a href="mailto:americangut@gmail.com">americangut@gmail.com</a>'
}

text_locale = {
    '404.html': _404,
    '403.html': _403,
    'FAQ.html': _FAQ,
    'introduction.html': _INTRODUCTION,
    'new_participant_overview.html': _NEW_PARTICIPANT_OVERVIEW,
    'nojs.html': _NOJS,
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
    'add_sample_overview.html': _ADD_SAMPLE_OVERVIEW,
    'participant_overview.html': _PARTICIPANT_OVERVIEW,
    'sample_overview.html': _SAMPLE_OVERVIEW,
    'basic_report.html': _BASIC_REPORT,
    'interactive_report.html': _INTERACTIVE_REPORT,
    'taxa_summary.html': _TAXA_SUMMARY,
    'map.html': _MAP,
    'register_user.html': _REGISTER_USER,
    'chage_pass_verify.html': _CHANGE_PASS_VERIFY,
    'survey_main.html': _SURVEY_MAIN,
    'animal_survey.html': _ANIMAL_SURVEY,
    'human_survey_completed.html': _HUMAN_SURVEY_COMPLETED,
    'handlers': _HANDLERS
}
