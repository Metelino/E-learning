from django.template.loader import render_to_string
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from .models import Course, Node, LessonFile, Question, Answer
from accounts.forms import LearningTypeForm
from .forms import (CourseForm, CourseSearchForm, CourseEditForm, NodeForm, NodeEditForm,
 FileForm, FileFormSet, QCreateForm, AnswerCreateFormSet, AnswerEditFormSet, QFormSet, QuestionForm)

# class ListCourses(ListView):
#     model = Course
#     template_name = 'courses/course-list.html'
def course_list(request):
    if request.method == 'POST':
        form = CourseSearchForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            #print(form)
            courses = None
            if form['category'] == 'wszystkie':
                courses = Course.objects.filter(name__contains=form['name'])
            else:
                courses = Course.objects.filter(category=form['category'], name__contains=form['name'])
            return render(request, 'courses/__courses.html', {'courses':courses})
    
    courses = Course.objects.all()
    form = CourseSearchForm()
    return render(request, 'courses/course-list.html', {'courses':courses, 'form':form})

def course_view(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    lessons = course.node_set.all()
    return render(request, 'courses/course-view.html', {'course':course, 'lessons':lessons})

@require_http_methods(['DELETE'])
@user_passes_test(lambda u: u.is_staff)
def course_delete(request, course_slug):
    try:
        course = Course.objects.get(slug=course_slug)
        if request.user.is_superuser or request.user == course.author:
            course.delete()
            return render(request, 'courses/__message.html', {'type':'is-success', 'title':'Pomyślnie usnięto kurs!'})
        return render(request, 'courses/__message.html', {'type':'is-danger', 'title':'Nie masz uprawnień!'})
    except:
        return render(request, 'courses/__message.html', {'type':'is-danger', 'title':'Nie udało się usunąć kursu!'})

@user_passes_test(lambda u: u.is_staff)
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
        return redirect('accounts:profile')
    else:
        form = CourseForm()
        return render(request, 'courses/course_add.html', {'form' : form})

@user_passes_test(lambda u: u.is_staff)
def course_edit(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if request.user != course.author:
        return redirect('courses:course_view', course_slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return render(request, 'courses/__message.html', {'type':'is-success', 'title':'Pomyślnie zmieniono opis!'})
        return render(request, 'courses/__message.html', {'type':'is-danger', 'title':'Nie udało się zmienić opisu!'})
    else:
        form = CourseForm(instance=course)
        lessons = course.node_set.all()
        return render(request, 'courses/course-edit.html', {'course':course , 'lessons':lessons, 'form':form})
    
@require_http_methods(['DELETE'])
@user_passes_test(lambda u: u.is_staff)
def node_delete(request, node_pk):
    #try:
        node = Node.objects.get(pk=node_pk)
        http = render(request, 'courses/__lesson.html', {'lesson': node, 'class':'scale-y-0', 'class':'scale-y-1', 'script':'on load toggle .y-0 on me\n on transitionend remove me'})
        #course = node.course
        if request.user.is_superuser or node.course.author == request.user:
            node.delete()
            http.write(render_to_string('courses/__message.html', {'title':'Usunięto lekcję!', 'type':'is-success'}))
            return http
        http.write(render_to_string('courses/__message.html', {'title':'Nie masz uprawnień!', 'type':'is-danger'}))
        return http
    # except:
    #     return render(request, 'courses/__message.html', {'title':'Nie udało się usunąć lekcji! Lekcja już nie istnieje.', 'type':'is-danger'})

@user_passes_test(lambda u: u.is_staff)
def test_edit(request, node):   
    questions = node.question_set.all()
    question_form = QCreateForm()
    answers_form = AnswerCreateFormSet(queryset=Answer.objects.none())
    return render(request, 'courses/test-edit.html', {'lesson':node, 'questions':questions, 'answers_form':answers_form, 'q_form':question_form})

@user_passes_test(lambda u: u.is_staff)
def lesson_edit(request, node):
    if request.method == 'POST':
        form = NodeEditForm(request.POST, instance=node)
        if form.is_valid():
            node.save()
            return render(request, 'courses/__message.html', {'type':'is-success', 'title':'Pomyślnie zmieniono opis!'})
        return render(request, 'courses/__message.html', {'type':'is-danger', 'title':'Zmiana opisu nieudana!'})

        #return redirect(request.META.get('HTTP_REFERER'))
    else:
        files = node.lessonfile_set.all()
        node_form = NodeEditForm(instance=node)
        files_form = FileForm()
        return render(request, 'courses/lesson-edit.html', {
            'lesson' : node,
            'files' : files, 
            'node_form' : node_form,
            'files_form' : files_form
            })

@require_http_methods(['POST'])
@user_passes_test(lambda u: u.is_staff)
def file_add(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    form = FileForm(request.POST, request.FILES) 
    lesson_file = None
    if form.is_valid():
        lesson_file = form.save(commit=False)
        lesson_file.node = node; lesson_file.save()
        http = render(request, 'courses/__edit_file.html', {'file':lesson_file, 'class':'scale-y-0', 'script':'on load toggle .y-1 on me'})
        http.write(render_to_string('courses/__message.html', {'title':'Plik dodano pomyślnie', 'type':'is-success'}))
        return http
    return render(request, 'courses/__message.html', {'title':'Błąd przy dodawaniu pliku', 'type':'is-danger'})
    

@require_http_methods(['DELETE'])
@user_passes_test(lambda u: u.is_staff)
def file_delete(request, file_pk):
    try:
        lesson_file = LessonFile.objects.get(pk=file_pk)
        http = render(request, 'courses/__edit_file.html', {'file':lesson_file, 'class':'scale-y-1', 'script':'on load toggle .y-0 on me\n on transitionend remove me'})
        lesson_file.lesson_file.delete() #usuwanie pliku w media
        lesson_file.delete()
        http.write(render_to_string('courses/__message.html', {'title':'Plik usnięto pomyślnie!', 'type':'is-success'}))
        return http
    except:
        return render(request, 'courses/__message.html', {'title':'Nie udało się usunąć pliku!', 'type':'is-danger'})
    #files = node.lessonfile_set.all()
    #return render(request, 'courses/__edit_files.html', {'files':files})

@user_passes_test(lambda u: u.is_staff)
def node_edit(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if request.user != node.course.author:
        return redirect('courses:node_view', node_pk)
    if node.node_type == 'lesson':
        return lesson_edit(request, node)
    else:
        return test_edit(request, node)

@user_passes_test(lambda u: u.is_staff)
def node_add(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if request.user != course.author:
        return redirect('courses:course_view', course_slug)
    if request.method == "POST":    
        form = NodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            node.course = course; node.save()
        return redirect('courses:course_edit', course_slug=course_slug)
    else:
        form = NodeForm()
        return render(request, 'courses/lesson-add.html', {'form' : form})

@login_required
def node_view(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if node.node_type == 'lesson':
        files = LessonFile.get_files(node, request.user.profile.learning_type)
        # files = files[request.user.profile.learning_type]
        l_form = LearningTypeForm(instance=request.user.profile)
        return render(request, 'courses/lesson-view.html', {'files':files, 'lesson':node, 'l_form':l_form})
    else:
        if request.method == 'POST':
            q_forms = QFormSet(request.POST)
            if q_forms.is_valid():
                points = 0
                max_points = node.question_set.count()
                for q in q_forms:
                    points += q.check_answers()
                if points == max_points:
                    request.user.profile.nodes_passed.add(node)
                #return redirect('courses:after_test', node_pk=node_pk, points=points, max_points=max_points)
                form = LearningTypeForm(instance = request.user.profile)
                return render(request,'courses/after_test.html', {'lesson':node, 'points':points, 'max_points':max_points, 'form':form})
                #return render(request, 'courses/after_test.html', {'passed':True, 'lesson':node}) 

        questions = node.question_set.all()
        q_forms = QFormSet(queryset=questions)
        return render(request, 'courses/test-view.html', {'lesson':node, 'q_forms':q_forms})

# @login_required
# def after_test(request, node_pk):
#     if request.user.profile.nodes_passed.filter(pk=node_pk).exists():
#         return render(request, 'courses/after_test.html', {'passed':True})
#     else:
#         return render(request, 'courses/after_test.html', {'passed':False})

@login_required
def lesson_passed(request, lesson_pk):
    try:
        lesson = Node.objects.get(pk=lesson_pk)
        request.user.profile.nodes_passed.add(lesson)
        http = HttpResponse()
        http['OK'] = True
        return http
    except:
        http = HttpResponse()
        http['OK'] = False
        return http

@login_required
def lesson_files(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    files = LessonFile.get_files(node, request.user.profile.learning_type)
    print(files)
    return render(request,'courses/__files.html', {'files':files})

@require_http_methods(['DELETE'])
@user_passes_test(lambda u: u.is_staff)
def question_delete(request, question_pk):
    try:
        q = Question.objects.get(pk=question_pk)
        http = render(request, 'courses/__question.html', {'q':q, 'class':'scale-y-1', 'script':'on load toggle .y-0 on me\n on transitionend remove me'})
        http.write(render_to_string('courses/__message.html', {'title':'Pytanie usunięto pomyślnie', 'type':'is-success'}))
        q.delete()
        return http
    except:
        return render(request, 'courses/__message.html', {'title':'Nie udało się dodać pytania!', 'type':'is-danger'})

@user_passes_test(lambda u: u.is_staff)
@require_http_methods(['POST'])
def question_add(request, test_pk):
    test = Node.objects.get(pk=test_pk)
    q_form = QCreateForm(request.POST)
    a_form = AnswerCreateFormSet(request.POST)
    q = None
    if q_form.is_valid():
        q = q_form.save(commit=False)
        q.node = test
        q.save()
        if a_form.is_valid():
            answers = a_form.save()
            for a in answers:
                q.answers.add(a)
            http =  render(request, 'courses/__question.html', {'q':q, 'class':'scale-y-0', 'script':'on load toggle .y-1 on me'})
            http.write(render_to_string('courses/__message.html', {'title':'Pytanie dodano pomyślnie', 'type':'is-success'}))
            return http
    return render(request, 'courses/__message.html', {'title':'Nie udało się dodać pytania!', 'type':'is-danger'})
    
@user_passes_test(lambda u: u.is_staff)
def question_update(request, question_pk):
    q = Question.objects.get(pk=question_pk)
    test = q.node
    if request.method == "GET":
        q_form = QCreateForm(instance=q)
        a_form = AnswerEditFormSet(queryset=q.answers.all(), prefix='edit_q')
        return render(request, 'courses/__question_update.html', {'q_form':q_form, 'a_form':a_form, 'q':q})
    if request.method =="POST":
        q_form = QCreateForm(request.POST, instance=q)
        a_form = AnswerEditFormSet(request.POST, queryset=q.answers.all(), prefix='edit_q')
        if q_form.is_valid():
            q_form.save()
            if a_form.is_valid():
                a_form.save()
                http = render(request, 'courses/__question.html', {'q':q})
                http.write(render_to_string('courses/__message.html', {'title':'Pytanie edytowane!', 'type':'is-success'})) 
                return http  
        return render(request, 'courses/__question.html', {'q':q})

@login_required
@xframe_options_exempt
def stream_file(request, file_pk):
    lesson_file = LessonFile.objects.get(pk=file_pk)
    return FileResponse(open(lesson_file.lesson_file.path, 'rb'))