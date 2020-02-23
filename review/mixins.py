from django.shortcuts import reverse, get_object_or_404, redirect, HttpResponseRedirect
from . models import Ratting, Movie
from . forms import RattingForm, CommentForm
from . get_ratings import GetRatings
from user.models import Profile
from django.contrib import messages
from . service.elasticsearch import search_for_movie

"""
                    Movie block
"""


class PostMovieMixin(object):
    
    def get_initial(self):
        return {
            'user' : self.request.user.id,
        }

    def form_valid(self, form):
        user = self.request.user
        profile = Profile.objects.get(user = user)
        action = self.request.POST.get('action')
        if not profile.confirmed:
            messages.error(self.request, 'Kindly activate your account')
            url = reverse('user:accountNotActivated')
            return redirect(to=url)
        if action == 'preview':
            ctx = self.get_context_data(form = form, preview = form.instance, action = action)
            return self.render_to_response(context = ctx)
        elif action == 'save':
            messages.success(self.request, self.success_message)
            return super().form_valid(form = form)

    def form_invalid(self, form):
        form_errors = form.errors
        ctx = self.get_context_data(form_errors = form_errors)
        return self.render_to_response(context = ctx)

class ManageMovieMixin(object):
    
    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        rating = Ratting.objects.get_rating_or_unsaved_rating(
            movie = self.object,
            user = self.request.user,
        )
        if rating.id:
            rated = True
            rating_form = RattingForm(instance = rating)
            rating_form_url = reverse(
                'review:updateRating',
                kwargs = {
                    'pk' : rating.id
                }
            )
        else:
            rated = False
            rating_form = RattingForm()
            rating_form_url = reverse(
                'review:postRating',
                kwargs = {
                    'pk' : self.object.id
                }
            )
        
        ctx.update({
            'comment_form': CommentForm(),
            'rating_form' : rating_form,
            'rating_form_url' : rating_form_url,
            'rated' : rated,
        })
        return ctx


"""
                    Comment block
"""


class CommentActionMixin(object):
    model = None
    choice = None

    def get_redirect_url(self, *args, **kwargs):
        id_ = self.kwargs['id']
        obj = get_object_or_404(self.model, id = id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if not user.profile.confirmed:
            messages.error(self.request, 'Kindly activate your account')
            url = reverse('user:accountNotActivated')
            return url
        if user.is_authenticated:
            if self.choice != None:
                if self.choice == 'like':
                    if user in obj.likes.all():
                        obj.likes.remove(user)
                    else:
                        obj.likes.add(user)
                        if user in obj.dislikes.all():
                            obj.dislikes.remove(user)
                        if user in obj.reports.all():
                            obj.reports.remove(user)

                if self.choice == 'dislike':
                    if user in obj.dislikes.all():
                        obj.dislikes.remove(user)
                    else:
                        obj.dislikes.add(user)
                        if user in obj.likes.all():
                            obj.likes.remove(user)
                if self.choice == 'report':
                    if user in obj.reports.all():
                        obj.reports.remove(user)
                    else:
                        if user in obj.likes.all():
                            obj.likes.remove(user)
                        obj.reports.add(user)
        return url_

class UpdateCreateCommentMixin(object):

    def get_object(self, queryset = None):
        comment = super().get_object(queryset)
        user = self.request.user
        if comment.user != user:
            raise PermissionError('Cannot change another users Vote!')
        return comment

    def get_initial(self):
        return {
            'user' : self.request.user,
            'movie' : self.get_movie().id,
        }

    def get_movie(self):
        if not self.update:
            id = self.kwargs['pk']
            return Movie.objects.get(id = id)
        else:
            id = self.get_object().movie.id
            return Movie.objects.get(id = id)

    def form_valid(self, form):
        if not self.request.user.profile.confirmed:
            messages.error(self.request, 'Kindly activate your account')
            url = reverse('user:accountNotActivated')
            return redirect(to = url)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        form_errors = form.errors
        ctx = self.get_context_data(form_errors = form_errors)
        return self.render_to_response(context = ctx)



"""
                    Rating block
"""


class PostRatingMixin(object):
    
    def get_initial(self):
        if self.update:
            return
        else:
            return {
                'user' : self.request.user,
                'movie' : self.kwargs.get('pk')
            }
    
    def get_object(self, queryset = None):
        rating = super().get_object(queryset)
        user = self.request.user
        if rating.user != user:
            raise PermissionError('Cannot change another users Vote!')
        return rating
    
    def form_valid(self, form):
        id = self.kwargs.get('pk')
        movie = Movie.objects.get(id = id)
        if movie.user == self.request.user:
            messages.error(self.request, "You are not allowed to rate on this Movie!")
            messages.error(self.request, "You're the author of this review")
        else:
            super().form_valid(form)
            if not self.update:
                messages.success(self.request, self.success_message)
            
            else:
                movie = self.get_object().movie
                movie.ratting = GetRatings.avg_rating(movie)
                movie.save()
                messages.warning(self.request, self.success_message)
        ctx = self.get_context_data()
        return self.render_to_response(context = ctx)

    def get_movie_id(self):
        id = self.get_object().movie.id
        return id
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        ctx = self.get_context_data()
        return self.render_to_response(context = ctx)

    def render_to_response(self, context, **response_kwargs):
        if self.update:
            movie_id = self.get_movie_id()
        else:
            movie_id = self.kwargs['pk']

        movie_detail_url = reverse('review:manage', kwargs={'pk': movie_id})
        return redirect(to = movie_detail_url)



"""
                    Rating block
"""

class SearchViewMixin(object):
    
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', None)
        ctx = super().get_context_data(query = query, **kwargs)
        if query:
            results = search_for_movie(query)
            ctx['hits'] = results
        return ctx