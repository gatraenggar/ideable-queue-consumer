from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

def send_email(payload_string):
    recipient_email = payload_string.split()[0]
    auth_token = payload_string.split()[1]

    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Verification for Registration"
    message["From"] = config("EMAIL_HOST_USER")
    message["To"] = recipient_email

    html_file = open("./templates/email_confirmation.html", 'r', encoding='utf-8')
    source_code = html_file.read().replace("{{url}}", config("API_URL") + "users/verification/" + auth_token)

    template = MIMEText(source_code, "html")

    message.attach(template)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(config("EMAIL_HOST_USER"), config("EMAIL_HOST_PASSWORD"))
        server.sendmail(
            message["From"], message["To"], message.as_string()
        )
