from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from uuid import uuid4
from review.models import Movie
from . import tasks

class Profile(models.Model):
    idConform = models.UUIDField(default = uuid4, editable = False)
    img = models.ImageField(default = 'img.jpg', upload_to = 'profile_pic')
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True)
    confirmed = models.BooleanField(default = False)
    notify = models.ManyToManyField(User, related_name = 'notifies', blank = True)
    email_send = False

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        if img.height > 300 and img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.img.path)

class Message(models.Model):
    message = models.CharField(max_length = 200)
    user = models.ForeignKey(to=User, on_delete = models.CASCADE)
    movie = models.ForeignKey(to = Movie, on_delete = models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = self._state.adding or force_insert
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        
        if is_new:
            tasks.make_subscriber_messages.delay(self.id)

class SubscriberMessageManager(models.Manager):
    def create_from_message(self, message):
        subscribers = message.user.profile.notify.all()
        return [
            self.create(message = message, subscriber = subscriber)
            for subscriber in subscribers
        ]


class SubscriberMessage(models.Model):
    message = models.ForeignKey(to = Message, on_delete = models.CASCADE)
    subscriber = models.ForeignKey(to = User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    send = models.DateTimeField(default = None, null = True)
    last_attempt = models.DateTimeField(default = None, null = True)
    seen = models.BooleanField(default = False)

    objects = SubscriberMessageManager()

    def __str__(self):
        return '{} message from {}'.format(self.subscriber, self.message.user)





