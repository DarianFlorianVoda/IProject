import smtplib
gmail_user = 'darivoda@gmail.com'
gmail_password = 'ce506e78'

sent_from = 'darivoda@gmail.com'
to = ['darian.voda00@e-uvt.ro']
subject = 'OMG Super Important Message'
body = "Hey, what's up?\n\n- Darian"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
except:
    print('Something went wrong...')
