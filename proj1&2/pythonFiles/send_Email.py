# libraries to be imported
import smtplib
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
load_dotenv('.env')

if not os.path.exists(r"public//sample_input//responses.csv"):
    print("please upload responses.csv file")
    exit()
with open(r"public//sample_input//responses.csv", 'r') as file:
    rows = csv.reader(file)
    addresses = {row[6]: [row[1], row[4]]
                 for row in rows if row[6] != "ANSWER" and row[6] != "Roll Number"}
a = 0
for key, values in addresses.items():
    a += 1
    if a == 5:
        break
    fromaddr = os.getenv('EMAIL_ADDRESS')
    toaddr = values

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = ", ".join(values)

    # storing the subject
    msg['Subject'] = "Automation_Begins"

    # string to store the body of the mail
    body = "First_automation assignment"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent
    filename = f"{key}.xlsx"
    attachment = open(rf"marksheets//{key}.xlsx", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, os.getenv('PASSWORD'))

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()
print("Sent mails successfully")
