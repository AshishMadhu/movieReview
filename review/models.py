from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from uuid import uuid4
from PIL import Image
from django.contrib import messages

import logging

logger =  logging.getLogger('django.request')


class MovieManager(models.Manager):
    def get_rating_range(self):
        return range(self.ratting)


class Movie(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    name = models.CharField(max_length = 240)
    poster = models.ImageField(upload_to = 'posters')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    ratting = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('review:manage', kwargs = {'pk' : self.id})

    def __str__(self):
        return f'{self.name}'

    def as_elasticsearch_dict(self):
        return {
            '_id' : self.id,
            '_type' : 'doc',
            'text' : '{} \n {}'.format(self.name, self.description),
            'movie_description' : self.description,
            'name' : self.name,
            'id' : self.id,
            'created' : self.date,
            'username' : self.user.username,
            'poster_url' : self.poster.url,
            'rating' : self.ratting,
        }

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        is_new = self._state.adding or force_insert
        super().save(force_insert = False, force_update = False, using = None, update_fields = None)

        img = Image.open(self.poster.path)

        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.poster.path)

        if is_new:
            self.create_message()
    
    def create_message(self):
        from user.models import Message
        Message.objects.create(user = self.user, message = f'{self.user} added a new movie review {self.name}', movie = self)



class Comment(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comment_likes', blank = True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comment_dislikes', blank = True)
    reports = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comment_reports', blank = True)

    def get_absolute_url(self):
        return reverse('review:manage', kwargs = {'pk': self.movie.id})

    def __str__(self):
        return f'{self.user} commented on {self.movie}'

class RatingManager(models.Manager):
    def get_rating_or_unsaved_rating(self, movie, user):
        try:
            return Ratting.objects.get(
                movie = movie,
                user = user
            )
        except Ratting.DoesNotExist:
            return Ratting(
                movie = movie,
                user = user,
            )

class Ratting(models.Model):
    choices = (
        (1, "💥"),
        (2, "💥💥"),
        (3, "💥💥💥"),
        (4, "💥💥💥💥"),
        (5, "💥💥💥💥💥"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.DO_NOTHING)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE, related_name = 'user_rating')
    ratted = models.IntegerField(default = 0, choices= choices)

    objects = RatingManager()

    class Meta:
        unique_together = ('user', 'movie')

    def get_absolute_url(self):
        return reverse('review:manage', kwargs = {'pk': self.movie.id})
    
    def __str__(self):
        return '{} ratted {}'.format(self.movie, self.ratted)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.user == self.movie.user:
            logger.error("you're the author so cannot rate on the movie")
        else:
            return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
