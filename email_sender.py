from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl, sys

sys.path.append("..")

def send_email(payload_string, routing_key):
    try:
        recipient_email = payload_string.split()[0]
        auth_token = payload_string.split()[1]

        services = {
            "email_confirmation": {
                "subject": "Email Verification for Registration",
                "template": "./templates/email_confirmation.html",
                "uri": "/email-verification/" + auth_token,
            },
            "workspace_invitation": {
                "subject": "Workspace Invitation by One of Your Friend",
                "template": "./templates/workspace_invitation.html",
                "uri": "/workspace-invitation/" + auth_token,
            }
        }

        message = MIMEMultipart("alternative")
        message["Subject"] = services[routing_key]["subject"]
        message["From"] = config("EMAIL_HOST_USER")
        message["To"] = recipient_email

        html_file = open(services[routing_key]["template"], 'r', encoding='utf-8')
        source_code = html_file.read().replace("{{url}}", config("CLIENT_URL") + services[routing_key]["uri"])

        template = MIMEText(source_code, "html")

        message.attach(template)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(config("EMAIL_HOST_USER"), config("EMAIL_HOST_PASSWORD"))
            server.sendmail(
                message["From"], message["To"], message.as_string()
            )
    except Exception as e:
        print(e)
        return
