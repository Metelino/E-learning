from django.db import models
from django.contrib import auth
from django.utils.text import slugify
from django.urls import reverse
from pathlib import Path

User = auth.get_user_model()

class LessonFile(models.Model):
    LESSON_TYPE = [
        ('0', 'Wzrokowiec'),
        ('1', 'Dzidowiec'),
        ('2', 'Słuchowiec'),
    ]

    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPE, default='0')
    lesson_file = models.FileField(upload_to='upload/', blank=True)

class Node(models.Model):
    NODE_TYPE = [
        ('lesson', 'Lekcja'),
        ('test', 'Test')
    ]
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    node_type = models.CharField(choices=NODE_TYPE, default='lesson', max_length=20)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class Question(models.Model):
    question_content = models.CharField(null=True, max_length=200)
    answers = models.CharField(null=True, max_length=30)

class Test(Node):
    questions = models.ManyToManyField(Question, blank=True)

class Lesson(Node):
    #name = models.CharField(max_length=100)
    files = models.ManyToManyField(LessonFile, related_name='learning_files', blank=True)
    #lesson_number = models.PositiveIntegerField(blank=True, null=True)
    #desc = models.CharField(max_length=1000)
    #slug = models.SlugField(allow_unicode=True, blank=True, null=True)

    def get_grouped_files(self):
        grouped_files = ['']
        files = self.files.all()
        for i in LessonFile.LESSON_TYPE:
            grouped_files.append(files.filter(lesson_type=i))
        return grouped_files

class Course(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor')
    nodes = models.ManyToManyField(Node, through='NodeInCourse')
    desc = models.CharField(max_length=1000)
    slug = models.SlugField(allow_unicode=True, blank=True, unique=True, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def add_node(self, node):
        NodeInCourse.objects.create(course = self.pk, node = node.pk)
        node.lesson_number = self.nodes.count()
        node.save()

    def get_course_view_url(self):
        return reverse('courses:course_view', self.slug)

    def get_course_edit_url(self):
            return reverse('courses:course_edit', self.slug)

class NodeInCourse(models.Model):
    course = models.ForeignKey(Course, related_name='lessons_course', on_delete=models.CASCADE)
    node = models.ForeignKey(Node, related_name='node_in_course', on_delete=models.CASCADE)
    node_number = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ['course', 'node']
        ordering = ('node_number',)

    @classmethod
    def add_lesson(self, node, course):
        x = self.objects.create(course=course, node=node)
        x.node_number = course.nodes.count()
        x.save()