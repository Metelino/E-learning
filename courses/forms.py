from django import forms
from .models import Course, Lesson, Node, LessonFile

class CourseForm(forms.ModelForm):
    class Meta():
        model = Course
        exclude = ['nodes', 'author', 'slug']
        labels = {
            'name' : 'Tytuł kursu',
            'desc' : 'Opis kursu'
        }
        widgets = {
            'name' : forms.TextInput(attrs = {'class' : 'input'}),
            'desc': forms.Textarea(attrs={'rows': 10, 'class':'textarea', 'style':'resize:none;'}),
        }

class CourseEditForm(forms.ModelForm):
    class Meta():
        model = Course
        exclude = ['nodes', 'author', 'slug']
        labels = {
            'name' : 'Tytuł kursu',
            'desc' : 'Opis kursu'
        }
        widgets = {
            'name' : forms.TextInput(attrs = {'class' : 'input'}),
            'desc': forms.Textarea(attrs={'rows': 10, 'class':'textarea', 'style':'resize:none;'}),
        }

class NodeForm(forms.ModelForm):
    node_choices = [
        ('test', 'Test'),
        ('lesson', 'Lekcja')
    ]
    class Meta():
        model = Node
        exclude = ['files', 'slug']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
            'node_type' : 'Rodzaj lekcji'
        }
        
class NodeEditForm(forms.ModelForm):
    node_choices = [
        ('test', 'Test'),
        ('lesson', 'Lekcja')
    ]
    class Meta():
        model = Node
        exclude = ['files', 'slug', 'node_type']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
        }

class LessonEditForm(forms.ModelForm):
    class Meta():
        model = Lesson
        exclude = ['files', 'slug']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
            'test' : 'Czy test'
        }

class FileForm(forms.ModelForm):
    class Meta():
        model = LessonFile
        fields = ['lesson_type', 'lesson_file']
        widgets = {
            'lesson_type' : forms.HiddenInput(),
            #'lesson_file' : forms.FileInput(attrs={'class':'file-input'})
        }
        labels = {
            'lesson_file' : ''
        }

FileFormSet = forms.formset_factory(FileForm, extra=0)
