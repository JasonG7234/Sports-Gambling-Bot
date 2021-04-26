import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(data):
    FROMADDR, FROMPASSWORD = get_login_info()
    TOADDR = "JasonG7234@gmail.com"

    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = "MLB Strikeout Props Error"
    MESSAGE['From'] = "variousemaillists@gmail.com"
    MESSAGE['To'] = TOADDR
    MESSAGE.preamble = '''
	Your mail reader does not support the format.
	'''
    HTML_BODY = MIMEText(data, 'html') #Record MIME type text/html
    MESSAGE.attach(HTML_BODY)
	
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(FROMADDR, FROMPASSWORD)
	
    server.sendmail(FROMADDR, TOADDR, MESSAGE.as_string())
		
    server.quit()

def get_login_info():
    f = open('keys.json')
    data = json.load(f)
    return data["email"], data["email_password"]