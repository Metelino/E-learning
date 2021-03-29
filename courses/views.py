from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Node, Lesson, Test, NodeInCourse, LessonFile
from .forms import CourseForm, CourseEditForm, NodeForm, NodeEditForm, LessonEditForm, FileFormSet

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
        lessons = course.nodes.all()
        return render(request, 'courses/course-edit.html', {'course_slug':course.slug , 'lessons':lessons, 'form':form})
    
@user_passes_test(lambda u: u.is_staff)
def node_delete(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if request.user.is_superuser or request.user == node.select_related('LessonInCourse').author:
        node.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def test_edit(request, node):   
    test = node.test
    return render(request, 'courses/test-edit.html')

def lesson_edit(request, node):
    lesson = node.lesson
    if request.method == 'POST':
        print('JESTEM W POST')
        form = NodeEditForm(request.POST)
        files_form = FileFormSet(request.POST, request.FILES)
        if form.is_valid():
            form = form.cleaned_data
            node.name = form['name']
            node.desc = form['desc']
            node.save()
        if files_form.is_valid():
            for inline_form in files_form:
                if inline_form.cleaned_data['lesson_file']:
                    lesson_file = inline_form.save()
                    lesson.files.add(lesson_file)
        else:
            print('ERROR')
            print(files_form.errors)
        #return redirect('courses:lesson_edit', lesson_pk=lesson.pk)
        return redirect(request.path_info)
    else:
        files = lesson.files.all()
        files_grouped = []
        for i in LessonFile.LESSON_TYPE:
            files_grouped.append(files.filter(lesson_type=i[0]))
        node_form = NodeEditForm(instance=node)
        files_form = FileFormSet(initial=[
            {'lesson_type' : '0'},
            {'lesson_type' : '1'},
            {'lesson_type' : '2'},
        ])
        return render(request, 'courses/lesson-edit.html', {
            'lesson' : lesson,
            'grouped_files' : files_grouped, 
            'node_form' : node_form,
            'files_form' : files_form
            })

def node_edit(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if node.node_type == 'lesson':
        return lesson_edit(request, node)
    else:
        return test_edit(request, node)

@user_passes_test(lambda u: u.is_staff)
def node_add(request, course_slug):
    if request.method == "POST":
        course = Course.objects.get(slug=course_slug)
        form = NodeForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['node_type'] == 'lesson':
                lesson = Lesson.objects.create(name = form['name'], desc=form['desc'], node_type=form['node_type'])
                NodeInCourse.add_lesson(lesson, course)
            else:
                test = Test.objects.create(name = form['name'], desc=form['desc'], node_type=form['node_type'])
                NodeInCourse.add_lesson(test, course)
        return redirect('courses:course_edit', course_slug=course_slug)
    else:
        form = NodeForm()
        return render(request, 'courses/lesson-add.html', {'form' : form})

def file_delete(request, file_pk):
    lesson_file = LessonFile.objects.get(pk=file_pk)
    lesson_file.lesson_file.delete()
    lesson_file.delete()
    return redirect(request.META.get('HTTP_REFERER'))