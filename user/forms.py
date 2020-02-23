from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.!')
        return email
    
    def save(self, *args, **kwargs):
        email = self.clean_email()
        super().save(*args, **kwargs)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2',]

class UpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']

class UserProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset= get_user_model().objects.all(),
        disabled = True,
        widget = forms.HiddenInput
    )

    class Meta:
        model = Profile
        fields = ['img', 'user']
        widgets = {
            'img': forms.FileInput(attrs = {'onchange': "upload()"})
        }
