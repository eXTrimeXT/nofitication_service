from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserContact

@receiver(post_save, sender=User)
def create_user_contact(sender, instance, created, **kwargs):
    if created:
        UserContact.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_contact(sender, instance, **kwargs):
    instance.usercontact.save()