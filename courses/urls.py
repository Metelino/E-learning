from django.urls import path
import django.contrib.auth.views as auth_views
from .views import (ListCourses, course_edit, course_add, course_view, 
node_add, node_edit, node_view, node_delete, file_delete, question_delete, question_add, stream_file)

app_name = 'courses'

urlpatterns = [
    path('course-list/', ListCourses.as_view(), name='course_list'),
    path('course-edit/<course_slug>', course_edit, name='course_edit'),
    path('course-view/<course_slug>', course_view, name='course_view'),
    path('course-add/', course_add, name='course_add'),
    #path('course-view/<course_slug>/', course_view, name='course_view'),
    #path('<course_slug>/lesson-view/<lesson_slug>/', lesson_view, name='lesson_view'),
    path('node-edit/<node_pk>/', node_edit, name='node_edit'),
    path('node-view/<node_pk>', node_view, name='node_view'),
    path('<course_slug>/node-add/', node_add, name='node_add'),
    path('node-delete/<node_pk>', node_delete, name='node_delete'),
    path('file-delete/<file_pk>', file_delete, name='file_delete'),
    #path('lesson-add/<slug>', course_detail, name='lesson_add'),
    path('question_delete/<question_pk>', question_delete, name='question_delete'),
    path('question_add/<test_pk>', question_add, name='question_add'),
    path('stream_file/<file_pk>', stream_file, name='stream_file')
]