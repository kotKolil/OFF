import smtplib

class MailClient(object):
    def __init__(self, SiteAdress, SitePort, MailLogin, MailPassword):
        self.Maillogin = MailLogin

        self.MailWorker = smtplib.SMTP('smtp.{SiteAdress}', SitePort)
        self.MailWorker.login(MailLogin,MailPassword)

    def SendMessage(self, TargetMail, text):
        self.MailWorker.sendmail(self.Maillogin, TargetMail, text)
        return 1