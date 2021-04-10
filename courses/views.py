from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse, FileResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Course, Node, LessonFile, Question, Answer
from accounts.forms import LearningTypeForm
from .forms import (CourseForm, CourseEditForm, NodeForm, NodeEditForm,
 FileForm, FileFormSet, QCreateForm, AnswerCreateFormSet, QFormSet, QuestionForm)

class ListCourses(ListView):
    model = Course
    template_name = 'courses/course-list.html'

@user_passes_test(lambda u: u.is_staff)
def course_delete(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if request.user.is_superuser or request.user == course.author:
        course.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda u: u.is_staff)
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
        return redirect('courses:course_list')
    else:
        form = CourseForm()
        return render(request, 'courses/course_add.html', {'form' : form})

@user_passes_test(lambda u: u.is_staff)
def course_edit(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if request.method == 'POST':
        form = CourseEditForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            course.name = form['name']
            course.desc = form['desc']
            course.save()
            return redirect('courses:course_edit', course.slug)
        else:
            print(form.errors)
            return HttpResponse('ERROR')
    else:
        form = CourseForm(instance=course)
        lessons = course.node_set.all()
        return render(request, 'courses/course-edit.html', {'course':course , 'lessons':lessons, 'form':form})

def course_view(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    lessons = course.node_set.all()
    return render(request, 'courses/course-view.html', {'course_slug':course.slug , 'lessons':lessons})
    
@user_passes_test(lambda u: u.is_staff)
def node_delete(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if request.user.is_superuser or request.user == node.select_related('LessonInCourse').author:
        node.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def test_edit(request, node):   
    questions = node.question_set.all()
    question_form = QCreateForm()
    answers_form = AnswerCreateFormSet(queryset=Answer.objects.none())
    return render(request, 'courses/test-edit.html', {'lesson':node, 'questions':questions, 'answers_form':answers_form, 'q_form':question_form})

def lesson_edit(request, node):
    if request.method == 'POST':
        form = NodeEditForm(request.POST, instance=node)
        if form.is_valid():
            node.save()
        return redirect(request.META.get('HTTP_REFERER'))
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

@user_passes_test(lambda u: u.is_staff)
def file_add(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES) 
        if form.is_valid():
            print("INSIDE FORM")
            lesson_file = form.save(commit=False)
            lesson_file.node = node; lesson_file.save()
            http = render(request, 'courses/__file.html', {'file':lesson_file})
            return http
    else:
        http = HttpResponse()
        http['OK'] = False
        return http
    #return redirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda u: u.is_staff)
def file_delete(request, file_pk):
    try:
        lesson_file = LessonFile.objects.get(pk=file_pk)
        lesson_file.lesson_file.delete()
        lesson_file.delete()
        return HttpResponse('OK')
    except:
        return HttpResponse('ERROR')

@user_passes_test(lambda u: u.is_staff)
def node_edit(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if node.node_type == 'lesson':
        return lesson_edit(request, node)
    else:
        return test_edit(request, node)

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
def node_view(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if node.node_type == 'lesson':
        files = LessonFile.get_files(node)
        files = files[request.user.profile.learning_type]
        l_form = LearningTypeForm(instance=request.user.profile)
        return render(request, 'courses/lesson-view.html', {'files':files, 'lesson':node, 'l_form':l_form})
    else:
        if request.method == 'POST':
            q_forms = QFormSet(request.POST)
            if q_forms.is_valid():
                print("PRZED FORMULARZEM")
                for q in q_forms:
                    if not q.check_answers():
                        return render(request, 'courses/after_test.html', {'passed':False, 'lesson':node})
                        #return HttpResponse("Zjebałeś!!")
                request.user.profile.nodes_passed.add(node)
                return render(request, 'courses/after_test.html', {'passed':True, 'lesson':node})
                #return HttpResponse("Dobrze!!")
                
            else:
                print(q_forms.errors)
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            questions = node.question_set.all()
            q_forms = QFormSet(queryset=questions)
            return render(request, 'courses/test-view.html', {'lesson':node, 'q_forms':q_forms})

@login_required
def after_test(request, node_pk):
    if request.user.profile.nodes_passed.filter(pk=node_pk).exists():
        return render(request, 'courses/after_test.html', {'passed':True})
    else:
        return render(request, 'courses/after_test.html', {'passed':False})


@user_passes_test(lambda u: u.is_staff)
def node_add(request, course_slug):
    if request.method == "POST":
        course = Course.objects.get(slug=course_slug)
        form = NodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            node.course = course; node.save()
        return redirect('courses:course_edit', course_slug=course_slug)
    else:
        form = NodeForm()
        return render(request, 'courses/lesson-add.html', {'form' : form})

@user_passes_test(lambda u: u.is_staff)
def question_delete(request, question_pk):
    q = Question.objects.get(pk=question_pk)
    q.delete()
    return redirect(request.META.get('HTTP_REFERER'))

# @user_passes_test(lambda u: u.is_staff)
# def question_add(request, test_pk):
#     if request.method == 'POST':
#         test = Node.objects.get(pk=test_pk)
#         #form = QCreateForm(request.POST)
#         q = Question.objects.create(node=test)
#         q.question_content = request.POST['question-content']
#         q_count = int(request.POST['question-count'])
#         answer = int(request.POST['answer'])
#         for i in range(q_count):
#             a = Answer.objects.create(text=request.POST[f'question-{i+1}'])
#             q.answer_fields.add(a)
#             if i == answer:
#                 q.answer = a
#         q.save()
#         #test.questions.add(q)
#     return redirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda u: u.is_staff)
def question_add(request, test_pk):
    if request.method == 'POST':
        test = Node.objects.get(pk=test_pk)
        q_form = QCreateForm(request.POST)
        a_form = AnswerCreateFormSet(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.node = test
            question.save()
            if a_form.is_valid():
                answers = a_form.save()
                for a in answers:
                    question.answers.add(a)
    return redirect(request.META.get('HTTP_REFERER'))

@xframe_options_exempt
def stream_file(request, file_pk):
    lesson_file = LessonFile.objects.get(pk=file_pk)
    return FileResponse(open(lesson_file.lesson_file.path, 'rb'))