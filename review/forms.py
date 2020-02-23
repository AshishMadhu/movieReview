from django import forms
from . models import Movie, Comment, Ratting
from django.contrib.auth import get_user_model
from . get_ratings import GetRatings
from django.shortcuts import HttpResponseRedirect 

class PostMovieForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset = get_user_model().objects.all(),
        widget = forms.HiddenInput,
        disabled = True
    )

    class Meta:
        model = Movie
        fields = ['user', 'name', 'poster', 'description']
        widgets = {
            'name' : forms.TextInput(attrs = {'autofocus' : True}),
            'poster': forms.FileInput(attrs = {'onchange': "previewFile()"})
        }

class CommentForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset = get_user_model().objects.all(),
        widget = forms.HiddenInput,
        disabled = True
    )
    movie = forms.ModelChoiceField(
        queryset = Movie.objects.all(),
        disabled = True,
        widget = forms.HiddenInput,
    )

    class Meta:
        model = Comment
        fields = ['user', 'movie', 'comment']

class RattingForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset = get_user_model().objects.all(),
        widget = forms.HiddenInput,
        disabled = True,
    )
    movie = forms.ModelChoiceField(
        queryset = Movie.objects.all(),
        disabled = True,
        widget = forms.HiddenInput,
    )

    class Meta:
        model = Ratting
        fields = ['user', 'movie', 'ratted']
