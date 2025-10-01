import smtplib as email_smtp
from email.mime.text import MIMEText
from email.header import Header
from ..config import EMAIL_LOGIN, EMAIL_PSWD

class EmailSender:
    @staticmethod
    def send(email, message):
        try:
            subject = 'Уведомление'
            text = message
            
            server = email_smtp.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_LOGIN, EMAIL_PSWD)
            
            mime = MIMEText(text, 'plain', 'utf-8')
            mime['Subject'] = Header(subject, 'utf-8')
            
            server.sendmail(EMAIL_LOGIN, email, mime.as_string())
            server.quit()
            print(f"Email отправлен на {email}")
            return True
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False