from . import mixins
from . models import Profile
from django.views import generic
from . forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(mixins.RegisterViewMixin, generic.CreateView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm

class ConfirmView(mixins.ConfirmViewMixin, generic.DetailView):
    model = Profile
    template_name = 'user/confirm_user_view.html'

class NotifyToggleView(LoginRequiredMixin,mixins.NotifyToggleViewMixin, generic.RedirectView):
    notify_toggle_view = True

class UserProfileView(LoginRequiredMixin, mixins.UserProfileViewMixin, generic.DetailView):
    model = User
    template_name = 'user/user_detail.html'

class UserMovieList(LoginRequiredMixin, mixins.UserMovieListMixin, generic.ListView):
    template_name = 'user/user_movie_list.html'
    ordering = ['-date']
    paginate_by = 10

class UserProfileUpdateView(LoginRequiredMixin, mixins.UserProfileUpdateViewMixin, generic.TemplateView):
    template_name = "user/profile_update.html"

class UserDpUpdateView(mixins.UserDpUpdateViewMixin, generic.RedirectView):
    user_dp_update = True

class MessageSeenRedirectView(mixins.MessageSeenRedirectViewMixin, generic.RedirectView):
    message_seen_view = True

class SubscriberListView(LoginRequiredMixin, mixins.SubscriberListViewMixin, generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'user/subscriber_list.html'
