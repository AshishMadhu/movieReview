from celery import shared_task
from review import emails
from django.contrib.auth.models import User

@shared_task
def send_confirmation_email(profile_id):
    from user.models import Profile
    profile = Profile.objects.get(id = profile_id)
    emails.send_confirmation_email(profile)

@shared_task
def make_subscriber_messages(message_id):
    print("In task")
    from user.models import Message, SubscriberMessage
    message = Message.objects.get(id = message_id)
    print(message)
    SubscriberMessage.objects.create_from_message(message)
    
