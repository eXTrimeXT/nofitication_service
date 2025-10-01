from django.contrib import admin
from .models import Notification, UserContact

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_short', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'created_at']
    actions = ['send_selected_notifications']
    
    def message_short(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_short.short_description = 'Сообщение'
    
    def send_selected_notifications(self, request, queryset):
        # Циклические импорты
        from .NotificationSender import NotificationSender
        
        service = NotificationSender()
        success_count = 0
        total_count = queryset.count()
        
        for notification in queryset:
            if service.send_notification(notification):
                success_count += 1
        
        self.message_user(
            request, 
            f"Успешно отправлено {success_count} из {total_count} уведомлений"
        )
    
    send_selected_notifications.short_description = "Отправить выбранные уведомления"

@admin.register(UserContact)
class UserContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_chat_id', 'email', 'phone']
    search_fields = ['user__username']