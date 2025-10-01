from django.utils import timezone
from django.apps import apps
from notifications.senders.EmailSender import EmailSender
from notifications.senders.SMSSender import SMSSender
from notifications.senders.TelegramSender import TelegramSender


class NotificationSender:
    def __init__(self):
        self.telegram_sender = TelegramSender()
        self.email_sender = EmailSender()
        self.sms_sender = SMSSender()

    def get_user_contact(self, user):
        UserContact = apps.get_model('notifications', 'UserContact') # Обход циклических импортов
        return UserContact.objects.filter(user=user).first()
    
    def send_notification(self, notification):
        user_contact = self.get_user_contact(notification.user)

        # Нет контактов
        if not user_contact:
            notification.status = 'failed'
            notification.save()
            return False
        
        # # Telegram
        if user_contact.telegram_chat_id:
            if self.telegram_sender.send(user_contact.telegram_chat_id, notification.message):
                notification.status = 'sent'
                notification.sent_at = timezone.now()
                notification.save()
                return True
        
        # Email
        if user_contact.email:
            if self.email_sender.send(user_contact.email, notification.message):
                notification.status = 'sent'
                notification.sent_at = timezone.now()
                notification.save()
                return True
        
        # SMS
        if user_contact.phone:
            if self.sms_sender.send(user_contact.phone, notification.message):
                notification.status = 'sent'
                notification.sent_at = timezone.now()
                notification.save()
                return True
        
        # Ничего не сработало
        notification.status = 'failed'
        notification.save()
        return False