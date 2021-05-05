from django.urls import path
import django.contrib.auth.views as auth_views
from .views import SignUp, user_profile, course_singup, change_learning, questionnairy_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', user_profile, name="profile"),
    path('course_signup/<course_slug>', course_singup, name="course_signup"),
    path('change_learning/', change_learning, name="change_learning"),
    path('questionnairy/', questionnairy_view, name='questionnairy')
]