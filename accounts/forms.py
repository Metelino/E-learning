from django import forms
from django.contrib import auth
from .models import Profile

class UserCreateForm(auth.forms.UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = auth.get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class LearningTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['learning_type']
        labels = {
            'learning_type' : 'Typ uczenia się'
        }