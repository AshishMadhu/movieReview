from django.shortcuts import reverse, Http404, redirect
from django.contrib import messages
from django.conf import settings
from . models import Profile, SubscriberMessage
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from . forms import UserRegisterForm, UserProfileForm, UpdateForm
from django.urls import  reverse_lazy
from review.models import Movie

class RegisterViewMixin(object):
    def get_success_url(self):
        messages.success(self.request, "Kindly check your email to Activate your Account!")
        return reverse(settings.LOGIN_URL)

class ConfirmViewMixin(object):

    def get_object(self, queryset = None):
        profile = Profile.objects.get(idConform = self.kwargs.get('pk'))
        profile.confirmed = True
        profile.save()
        return profile


class UserProfileViewMixin(object):
    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        try:
            obj = User.objects.get(username = username)
            return obj
        except:
            raise Http404
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p_form = UserProfileForm()
        url = reverse_lazy('user:updateProfile', kwargs = {'username' : self.request.user})
        current_user = self.request.user
        user = self.get_object()
        user_messages = SubscriberMessage.objects.filter(subscriber = current_user, seen = False).order_by('-created')[:15]
        if current_user in user.profile.notify.all():
            subscribe = True
        else:
            subscribe = False
        ctx.update({
            'p_form' : p_form,
            'url' : url,
            'current_user' : current_user, 
            'subscribe' : subscribe,
            'user_messages' : user_messages,
        })
        return ctx


class NotifyToggleViewMixin(object):
    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get('username')
        user = self.request.user
        try:
            review_user = User.objects.get(username = username)
        except ObjectDoesNotExist:
            raise PermissionDenied()
        if user in review_user.profile.notify.all():
            review_user.profile.notify.remove(user)
        else:
            review_user.profile.notify.add(user)
        url = reverse('user:profile', kwargs = {'username': review_user})
        return url

class UserMovieListMixin(object):
    
    def get_queryset(self):
        qs = Movie.objects.filter(user = self.request.user)
        return qs

class UserProfileUpdateViewMixin(object):
    
    def get(self, request, *args, **kwargs):
        if self.request.user.username != self.kwargs.get('username'):
            raise PermissionDenied("You are not allowed to access")
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        u_form = UpdateForm(instance = self.request.user)
        p_form = UserProfileForm(instance = self.request.user.profile)
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'u_form' : u_form,
            'p_form' : p_form
        })
        return ctx

    def post(self, request, *args, **kwargs):
        u_form = UpdateForm(request.POST, instance = request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "You have updated your porfile!!")
            url = reverse('user:profile', kwargs = {'username' : request.user.username})
            return redirect(to=url)
        else:
            u_form_errors = u_form.errors
            if u_form_errors:
                print(u_form_errors)
            else:
                print("no errors")
            p_form_errors = p_form.errors
            ctx = self.get_context_data()
            ctx.update({
                'form_errors' : u_form_errors,
            })
            return self.render_to_response(context = ctx)

class UserDpUpdateViewMixin(object):

    def post(self, *args, **kwargs):
        return self.get_redirect_url(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        url = self.updateUserInfo(self.request)
        return url

    def updateUserInfo(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("You are not allowed to access!!")
        else:
            if request.method == 'POST':
                p_form = UserProfileForm(request.POST, request.FILES, instance = request.user.profile)

                if p_form.is_valid():
                    p_form.save()
                    messages.success(request, 'Your Profile Photo is changed, OH YEAH!!!')
                else:
                    print(p_form.errors)

                return redirect('user:profile', username = request.user.username)
            
            else:
                url = reverse('user:updateProfile', kwargs = {'username' : request.user.username})
                return url


class MessageSeenRedirectViewMixin(object):
    def get_redirect_url(self, *args, **kwargs):
        from user.models import SubscriberMessage
        message_id = self.kwargs.get('pk')
        message = SubscriberMessage.objects.get(id = message_id)
        message.seen = True
        message.save()
        url = reverse('review:manage', kwargs = {'pk' : message.message.movie.id})
        return url

class SubscriberListViewMixin(object):
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = self.model.objects.get(username = username)
        qs = user.profile.notify.all()
        return qs