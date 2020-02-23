from django.core.management import BaseCommand
from review.service import elasticsearch
from review.models import Movie

class Command(BaseCommand):
    help = 'Load all the movies to elasticsearch index'

    def handle(self, *args, **options):
        queryset = Movie.objects.all()
        all_loaded = elasticsearch.bulk_load(queryset)
        if all_loaded:
            self.stdout.write(self.style.SUCCESS(
                'Successfully loaded all the movies to ElasticSearch index.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'Some movies are not loaded successfully. See logged errors.'
            ))