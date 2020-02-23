from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('pass-reset/', auth_views.PasswordResetView.as_view(
            template_name = 'registration/password_reset.html',
            success_url = reverse_lazy('user:password_reset_done'),
            html_email_template_name = 'registration/password_reset_email.html'
            ), name = 'password_rest'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_success.html'), name='password_reset_done'),
    path('pass-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url = reverse_lazy('user:password_reset_complete')
            ), name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('uploads/', views.UserMovieList.as_view(), name = 'userUploads'),
    path('notactivated/', TemplateView.as_view(template_name = 'user/not_activated.html'), name = 'accountNotActivated'),
    path('<slug:username>/subscribers/', views.SubscriberListView.as_view(), name ='subscriberList'),
    path('<uuid:pk>/confirm/', views.ConfirmView.as_view(), name = 'confirmUser'),
    path('<slug:username>/notify/', views.NotifyToggleView.as_view(), name = 'notify'),
    path('image/update/', views.UserDpUpdateView.as_view(), name = 'updateProfileImage'),
    path('profile/<slug:username>/', views.UserProfileView.as_view(), name = 'profile'),
    path('<int:pk>/seen/', views.MessageSeenRedirectView.as_view(), name = 'seen'),
    path('profile/<slug:username>/update/', views.UserProfileUpdateView.as_view(), name = "updateProfile"),
]