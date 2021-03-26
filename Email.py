import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

gmail_user = 'darivoda@gmail.com'
gmail_password = 'ce506e78'
sent_from = 'darivoda@gmail.com'
to = ['darian.voda00@e-uvt.ro']
subject = 'COVID-19 Charts - Project'
body = "Hello\n\n This is a mail which contains 3 charts relating to COVID-19 cases worldwide. Enjoy!\n\n- Darian"


msg = MIMEMultipart()
msg['From'] = sent_from
msg['To'] = gmail_user
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

msg.attach(MIMEText(body,'plain'))

with open(r'C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\barchart.png', 'rb') as fp:
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition','attachment',filename=r"C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\barchart.png")

msg.attach(img)

with open(r'C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\piechart.png', 'rb') as fp:
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition','attachment',filename=r"C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\piechart.png")

msg.attach(img)

with open(r'C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\scatter.png', 'rb') as fp:
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition','attachment',filename=r"C:\Users\Dari-PC\PycharmProjects\IProject2\Covid19Stats\scatter.png")

msg.attach(img)

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
    server.sendmail(sent_from, to, msg.as_string())
    server.close()
except:
    print('Something went wrong...')
