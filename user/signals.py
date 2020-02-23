from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Profile
from . tasks import send_confirmation_email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        send_confirmation_email.delay(profile.id)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()