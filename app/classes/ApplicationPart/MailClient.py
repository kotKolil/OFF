import smtplib as smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient(object):
    def __init__(self, SiteAddress, SitePort, MailLogin, MailPassword, ForumName, logger):
        self.logger = logger

        try:
            self.ForumName = ForumName
            self.MailLogin = MailLogin
            self.server = smtp.SMTP(SiteAddress, SitePort)
            self.server.starttls()
            self.server.login(MailLogin, MailPassword)

        except smtp.SMTPServerDisconnected:
            logger.error("Mail Worker not initialized")
        except Exception as e:
            logger.error("An error occurred while initializing the mail client: {}".format(e))

    def send_message(self, TargetMail, text, Theme):
        # Create a multipart message
        msg = MIMEMultipart()

        # Set the sender's name and email
        msg['From'] = "{} <{}>".format(self.ForumName, self.MailLogin)
        msg['To'] = TargetMail
        msg['Subject'] = Theme

        # Attach the message body
        msg.attach(MIMEText(text, 'plain'))

        try:
            # Send the message
            self.server.sendmail(self.MailLogin, TargetMail, msg.as_string())
            return 1
        except Exception as e:
            self.logger.error("Failed to send email to {}: {}".format(TargetMail, e))
            return 0  # Indicate failure in sending the email

    def close(self):
        """Close the SMTP server connection."""
        try:
            self.server.quit()
        except Exception as e:
            self.logger.error("Failed to close the mail server connection: {}".format(e))
