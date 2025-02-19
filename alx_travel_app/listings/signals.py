from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")

