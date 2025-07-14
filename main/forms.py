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


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    ('A', question.option_a),
                    ('B', question.option_b),
                    ('C', question.option_c),
                    ('D', question.option_d)
                ],
                widget=forms.RadioSelect,
                required=True
            )