from __future__ import division

import smtplib
from email.mime.text import MIMEText
from amgut.lib.locale_data.american_gut import media_locale


def send_email(message, subject, recipient='americangut@gmail.com',
               sender=None):
    """Send an email from your local host """
    if sender is None:
        sender = media_locale['HELP_EMAIL']
    # Create a text/plain message
    msg = MIMEText(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [recipient], msg.as_string())
    s.quit()
