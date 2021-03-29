from django.urls import path
import django.contrib.auth.views as auth_views
from .views import SignUp

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]