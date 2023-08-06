import smtplib, ssl
from email.message import EmailMessage
import os
import socket


class EmailAlerts:
    def __init__(self, smtp_address, email_port, email_sender, email_password, email_receiver):
        self.environment = None
        self.message = None
        self.subject = None
        self.smtp_address = smtp_address
        self.email_password = email_password
        self.email_port = email_port
        self.email_sender = email_sender
        self.email_receiver = email_receiver

    def send_email(self, subject, body):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver
        msg.set_content(body)

        with smtplib.SMTP(self.smtp_address, self.email_port) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(self.email_sender, self.email_password)
            smtp.send_message(msg)
            print("Email sent successfully")

    def set_message(self, message):
        self.message = message

    def set_subject(self, subject):
        self.subject = subject

    def set_environment(self, environment):
        self.environment = environment

    def set_email_alert_info(self, subject, message, environment):
        """
        Set the message, subject and environment for the email alert all in one function.
        """
        self.set_environment(environment)
        self.set_message(message)
        self.set_subject(subject)

    def reset_email_alert_info(self):
        """
        Reset the email alert info to default values.
        """
        self.set_message(None)
        self.set_subject(None)
        self.set_environment(None)

    def email_alert_decorator(self, fnc):
        """
        Wrapper function for email alerts. The contents of the email can be set by the user
        using the set_message set_subject functions, and set_environment function.
        If None is passed to any of these functions, the default values will be used.
        """

        def wrapper(*args, **kwargs):
            try:
                return fnc(*args, **kwargs)
            except Exception as e:
                if self.environment is None:
                    self.environment = "Production"
                if self.message is None:
                    self.message = \
                        f"ERROR: {e}\n\
                        DEVICE: {socket.gethostname()}\n\
                        FILE: {os.path.abspath(__file__)}\n\
                        "
                if self.subject is None:
                    self.subject = f"Email alert: Error in: {self.environment}"

                self.send_email(self.subject, self.message)

        return wrapper
