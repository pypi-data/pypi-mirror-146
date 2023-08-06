from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pytomlpp


class Client(smtplib.SMTP):
    def __init__(self, host, user, password, port=587):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.smtp_client = self._init_client()

    def _init_client(self):
        s = smtplib.SMTP(self.host, self.port)
        s.ehlo()
        s.starttls()
        s.ehlo()

        try:
            s.login(self.user, self.password)
            return s
        except smtplib.SMTPAuthenticationError:
            print("Authentication failed. Check your configuration and try again.")

    def create_message(self, from_addr, to_addr, body, subject="No subject"):
        msg = MIMEMultipart()
        msg.add_header("From", from_addr)
        msg.add_header("To", to_addr)
        msg.add_header("Subject", subject)
        msg.attach(MIMEText(body))
        return msg

    def send_message(self, from_addr, to_addr, msg):
        res = self.smtp_client.sendmail(from_addr, to_addr, msg.as_bytes())
        return res
