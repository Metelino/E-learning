from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse, FileResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Course, Node, LessonFile, Question, Answer
from accounts.models import UserInCourse
from .forms import CourseForm, CourseEditForm, NodeForm, NodeEditForm, FileFormSet, QCreateForm, QFormSet, QuestionForm

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
        return render(request, 'courses/course-edit.html', {'course_slug':course.slug , 'lessons':lessons, 'form':form})

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
    return render(request, 'courses/test-edit.html', {'lesson':node, 'questions':questions})

def lesson_edit(request, node):
    if request.method == 'POST':
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
                    lesson_file = inline_form.save(commit=False)
                    lesson_file.node = node; lesson_file.save()
        else:
            print('ERROR')
            print(files_form.errors)
        #return redirect('courses:lesson_edit', lesson_pk=lesson.pk)
        return redirect(request.path_info)
    else:
        files = node.lessonfile_set.all()
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
            'lesson' : node,
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

def lesson_passed(request, lesson_pk):
    lesson = Lesson.objects.get(pk=lesson_pk)
    course = lesson.course_set.first()
    user_course = UserInCourse.objects.get(course=course, user=request.user)
    user_course.lessons_passed[lesson_pk] = True
    return redirect(request.META.get('HTTP_REFERER'))

def node_view(request, node_pk):
    node = Node.objects.get(pk=node_pk)
    if node.node_type == 'lesson':
        files = LessonFile.get_files(node)
        files = files[request.user.info.learning_type]
        return render(request, 'courses/lesson-view.html', {'files' : files, 'lesson':node})
    else:
        if request.method == 'POST':
            q_forms = QFormSet(request.POST)
            print("DZIALA")
            if q_forms.is_valid():
                # print("FORMULARZ DZIALA")
                # for form in q_forms:
                #     if not test.check_answer(form.cleaned_data['answer']):
                #         break
                # else:
                #     course = node.course_set.first()
                #     user_course = UserInCourse.objects.get(course=course, user=request.user)
                #     user_course.lessons_passed[node_pk] = True
                return render(request, 'courses/after_test.html')
            else:
                print(q_forms.errors)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            questions = node.question_set.all()
            q_forms = QFormSet(queryset=questions)
            return render(request, 'courses/test-view.html', {'lesson':node, 'q_forms':q_forms})
    


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

def question_delete(request, question_pk):
    q = Question.objects.get(pk=question_pk)
    q.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def question_add(request, test_pk):
    if request.method == 'POST':
        test = Node.objects.get(pk=test_pk)
        #form = QCreateForm(request.POST)
        q = Question.objects.create(node=test)
        q.question_content = request.POST['question-content']
        q_count = int(request.POST['question-count'])
        answer = int(request.POST['answer'])
        for i in range(q_count):
            a = Answer.objects.create(text=request.POST[f'question-{i+1}'])
            q.answer_fields.add(a)
            if i == answer:
                q.answer = a
        q.save()
        #test.questions.add(q)
    return redirect(request.META.get('HTTP_REFERER'))

def file_delete(request, file_pk):
    lesson_file = LessonFile.objects.get(pk=file_pk)
    lesson_file.lesson_file.delete()
    lesson_file.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@xframe_options_exempt
def stream_file(request, file_pk):
    lesson_file = LessonFile.objects.get(pk=file_pk)
    return FileResponse(open(lesson_file.lesson_file.path, 'rb'))