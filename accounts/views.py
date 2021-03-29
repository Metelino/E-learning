from django.shortcuts import render
from django.urls import reverse_lazy
#from django.contrib import auth
from .forms import UserCreateForm
from django.views.generic import CreateView

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name='accounts/signup.html'

# Create your views here.
