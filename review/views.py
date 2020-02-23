from django.views.generic import CreateView, DetailView, ListView, UpdateView, RedirectView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import PostMovieForm, CommentForm, RattingForm
from django.contrib.messages.views import SuccessMessageMixin
from . models import Movie, Ratting, Comment
from . import mixins


class PostMovieView(LoginRequiredMixin, mixins.PostMovieMixin, CreateView):
    form_class = PostMovieForm
    template_name = 'review/post_movie.html'
    success_message = 'Successfully posted the movie.'

class ManageMovie(LoginRequiredMixin, mixins.ManageMovieMixin, DetailView):
    model = Movie

class MovieListView(ListView):
    model = Movie
    ordering = ['-date']
    paginate_by = 10

# Comment block

class PostCommentView(LoginRequiredMixin, mixins.UpdateCreateCommentMixin, CreateView):
    form_class = CommentForm
    template_name = 'review/create_comment.html'
    success_message = "You have posted a comment!"
    update = False

class UpdateCommentView(mixins.UpdateCreateCommentMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'review/comment_update_form.html'
    success_message = 'Your Comment has been updated!'
    update = True

class CommentLikeToggleView(mixins.CommentActionMixin, RedirectView):
    model = Comment
    choice = 'like'

class CommentDislikeToggleView(mixins.CommentActionMixin, RedirectView):
    model = Comment
    choice = 'dislike'

class CommentReportToggleView(mixins.CommentActionMixin, RedirectView):
    model = Comment
    choice = 'report'

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        obj = self.get_object()
        url = obj.movie.get_absolute_url()
        return url

# Rating block

class PostRatingView(LoginRequiredMixin, mixins.PostRatingMixin, CreateView):
    form_class = RattingForm
    success_message = "Thanks for your valuable rating"
    update = False

class UpdateRatingView(LoginRequiredMixin, mixins.PostRatingMixin, UpdateView):
    model = Ratting
    form_class = RattingForm
    success_message = "Your Ratting has been updated"
    update = True

# Search

class SearchView(mixins.SearchViewMixin, TemplateView):
    template_name = 'review/search.html' 

# About

class AboutView(TemplateView):
    template_name = 'review/about.html'