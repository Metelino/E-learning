from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
#from django.contrib import auth
from .forms import UserCreateForm, LearningTypeForm
from django.views.generic import CreateView
#from .models import UserInCourse
from courses.models import Course

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name='accounts/signup.html'

def user_profile(request):
    courses = request.user.profile.courses.all()
    return render(request, 'accounts/profile.html', {'courses':courses})

def course_singup(request, course_slug):
    try:
        course = Course.objects.get(slug=course_slug)
        request.user.profile.courses.add(course)
        # UserInCourse.objects.create(user=request.user.profile, course=course)
        return HttpResponse('OK')
    except:
        return HttpResponse('ERROR')

def change_learning(request):
    if request.method == 'POST':   
        form = LearningTypeForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER'))
