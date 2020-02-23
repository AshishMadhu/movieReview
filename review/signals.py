from django.db.models.signals import post_save
from . models import Ratting, Movie
from django.dispatch import receiver
from . get_ratings import GetRatings

@receiver(post_save, sender = Ratting)
def update_rating(sender, instance, created, **kwargs):
    if created:
        movie = instance.movie
        movie.ratting = GetRatings().avg_rating(movie)
        movie.save()
