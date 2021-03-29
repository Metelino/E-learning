from django.forms import ModelForm
from django.contrib import auth

class UserCreateForm(auth.forms.UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = auth.get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
    