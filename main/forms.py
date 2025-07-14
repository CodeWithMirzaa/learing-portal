from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import Video

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['product', 'title', 'youtube_url', 'order']