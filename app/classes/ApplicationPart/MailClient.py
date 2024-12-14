import smtplib as smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailClient(object):
    def __init__(self, SiteAdress, SitePort, MailLogin, MailPassword, ForumName, logger):

        self.logger = logger

        try:

            self.ForumName = ForumName
            self.MailLogin = MailLogin
            self.server = smtp.SMTP(SiteAdress, SitePort)
            self.server.starttls()
            self.server.login(MailLogin, MailPassword)

        except smtp.SMTPServerDisconnected:

            logger.error("Mail Worker not inited")


    def SendMessage(self, TargetMail, text, Theme):
        # Create a multipart message
        msg = MIMEMultipart()
        
        # Set the sender's name and email
        msg['From'] = f"{self.ForumName} <{self.MailLogin}>"
        msg['To'] = TargetMail
        msg['Subject'] = Theme        
        # Attach the message body
        msg.attach(MIMEText(text, 'plain'))
        
        # Send the message
        self.server.sendmail(self.MailLogin, TargetMail, msg.as_string())
        return 1

