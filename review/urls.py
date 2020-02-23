from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'review'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name = 'about'),
    path('post/', views.PostMovieView.as_view(), name = 'post'),
    path('movielist/', views.MovieListView.as_view(), name = 'movieList'),
    path('<uuid:pk>/manage/', views.ManageMovie.as_view(), name = 'manage'),
    path('<uuid:pk>/post/comment/', views.PostCommentView.as_view(), name = 'postComment'),
    path('<uuid:pk>/update/comment/', views.UpdateCommentView.as_view(), name = 'updateComment'),
    path('<uuid:pk>/delete/comment/', views.DeleteCommentView.as_view(), name = 'deleteComment'),
    path('<uuid:id>/like/', views.CommentLikeToggleView.as_view(), name = 'commentLike'),
    path('<uuid:id>/dislike/', views.CommentDislikeToggleView.as_view(), name = 'commentDislike'),
    path('<uuid:id>/report/', views.CommentReportToggleView.as_view(), name = 'commentReport'),
    path('<uuid:pk>/rate/', views.PostRatingView.as_view(), name = 'postRating'),
    path('<int:pk>/update/rating/', views.UpdateRatingView.as_view(), name = 'updateRating'),
    path('movie/search', views.SearchView.as_view(), name = 'search'),
]