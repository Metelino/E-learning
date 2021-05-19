from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib import auth
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from pathlib import Path


User = auth.get_user_model()

class VAK(models.TextChoices):
    WZROKOWIEC = '0', _('Wzrokowiec')
    KINESTETYK = '1', _('Kinestetyk')
    SLUCHOWIEC = '2', _('Słuchowiec')

def get_upload_path(instance, filename):
    return f'node_{instance.node.id}_files/{filename}'

class LessonFile(models.Model):
    LESSON_TYPE = [
        ('0', 'Wzrokowiec'),
        ('1', 'Kinestetyk'),
        ('2', 'Słuchowiec'),
    ]
    lesson_type = MultiSelectField(max_length=5, choices=VAK.choices, default='0')
    # lesson_type = models.CharField(max_length=20, choices=VAK.choices, default='0')
    lesson_file = models.FileField(upload_to=get_upload_path)
    node = models.ForeignKey(to='Node', on_delete=models.CASCADE)

    def get_name(self):
        p = Path(self.lesson_file.path)
        return p.stem

    @classmethod
    def get_files(self, node, lesson_type):
        files = self.objects.filter(node = node, lesson_type__contains=lesson_type)
        return files

    def get_absolute_url(self):
        return reverse('courses:stream_file', kwargs={'file_pk':self.pk})

class Answer(models.Model):
    text = models.CharField(max_length=100, null=True)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.text)

class Question(models.Model):
    text = models.CharField(null=True, max_length=200)
    answers = models.ManyToManyField(Answer)
    node = models.ForeignKey(to='Node', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.text)

    def delete(self, *args, **kwargs):
        for a in self.answers.all():
            a.delete()
        super().delete(*args, **kwargs)

class Node(models.Model):
    NODE_TYPE = [
        ('lesson', 'Lekcja'),
        ('test', 'Test')
    ]
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    content = models.CharField(max_length=2000, default='')
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)
    node_type = models.CharField(choices=NODE_TYPE, default='lesson', max_length=20)
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE)
    node_number = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.node_number = self.course.node_count
            self.course.node_count += 1
            self.course.save()

        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_prev(self):
        return Node.objects.get(course=self.course, node_number=self.node_number-1)

    def delete(self, *args, **kwargs):
        self.course.node_count -= 1
        self.course.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta():
        unique_together = ['course', 'node_number']


class Course(models.Model):
    CATEGORIES = [
        ('other', 'inna'),
        ('infa', 'informatyka'),
        ('matma', 'matematyka'),
        ('fizyka', 'fizyka'),
        ('biologia', 'biologia'),
        ('chemia', 'chemia')
    ]
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_courses')
    category = models.CharField(choices=CATEGORIES, default='other', max_length=100)
    desc = models.CharField(max_length=1000)
    slug = models.SlugField(allow_unicode=True, blank=True, unique=True, null=True)
    node_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)

    def get_last_node(self):
        try:
            return self.node_set.get(node_number=self.node_count-1).pk
        except:
            return None
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
