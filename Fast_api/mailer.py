import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Set your SendGrid API key
mail_key= "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"
sg = SendGridAPIClient(mail_key)

def send_email(subject, message, to_email):
    message = Mail(
        from_email='iam7668ok@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=message)

    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

# Example usage
# send_email("Subject", "Hello, this is a test email.", "sonumandal048@gmail.com")
