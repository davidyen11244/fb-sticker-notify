#!/usr/bin/python
# -*- encoding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendHtmlEmail(to, title, content):
    msg = MIMEText(content, 'html')
    msg['From'] = 'YOUR_EMAIL'
    msg['To'] = ', '.join(to)
    msg['Subject'] = title

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login('YOUR_ACCOUNT', 'YOUR_PASSWORD')
    s.sendmail('YOUR_EMAIL', to, msg.as_string())
    s.quit()
