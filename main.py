import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'mail.proxyitsupport.com'     # Your mail server
SMTP_PORT = 587                              # Use 465 for SSL
YOUR_EMAIL = 'interview@proxyitsupport.com'
YOUR_PASSWORD = 'your_email_password'
SUBJECT = "Interview Invitation"

with open('email_template.txt', 'r') as file:
    template = file.read()

with open('data/recipients.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    recipients = list(reader)

try:
    if SMTP_PORT == 465:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    else:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

    server.login(YOUR_EMAIL, YOUR_PASSWORD)
    print("✅ Connected to SMTP server.")

    for person in recipients:
        name = person['name']
        email = person['email']
        personalized_message = template.format(name=name)

        msg = MIMEMultipart()
        msg['From'] = YOUR_EMAIL
        msg['To'] = email
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(personalized_message, 'plain'))

        server.send_message(msg)
        print(f"📤 Sent email to {name} ({email})")

    server.quit()
    print("✅ All emails sent successfully.")

except Exception as e:
    print("❌ Failed to send emails. Error:", e)
