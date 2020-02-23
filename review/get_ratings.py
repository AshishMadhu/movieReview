from .models import Ratting

class GetRatings():

    @classmethod
    def get_ratings_count(self, movie):
        qs = Ratting.objects.filter(movie = movie)
        rating_1 = qs.filter(ratted = '1').count() 
        rating_2 = qs.filter(ratted = '2').count()
        rating_3 = qs.filter(ratted = '3').count()
        rating_4 = qs.filter(ratted = '4').count()
        rating_5 = qs.filter(ratted = '5').count()
        obj = {
            'rating_1' : rating_1,
            'rating_2' : rating_2,
            'rating_3' : rating_3,
            'rating_4' : rating_4,
            'rating_5' : rating_5,
        }
        return obj

    @classmethod
    def avg_rating(self, movie):
        obj = self.get_ratings_count(movie)
        total_starts = (1 * obj['rating_1']) + (2 * obj['rating_2']) + (3 * obj['rating_3']) + (4 * obj['rating_4']) + (5 * obj['rating_5'])
        number_of_starts = obj['rating_1'] + obj['rating_2'] + obj['rating_3'] + obj['rating_4'] + obj['rating_5']
        avg = total_starts / number_of_starts
        return avg

