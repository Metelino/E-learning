from django import forms
from .models import Course, Node, LessonFile, Question

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
        exclude = ['files', 'slug', 'course']
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
        exclude = ['files', 'slug', 'node_type', 'course']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
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

class QCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_content', 'answer_fields', 'answer']
        widgets = {
            'question_content' : forms.HiddenInput(attrs={'id':'real_content'}),
            'answer_fields' : forms.HiddenInput(attrs={'id':'real_fields'}),
            'answer' : forms.HiddenInput(attrs={'id':'real_answer'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta():
        fields = ['answer_fields']
        widgets = {'answer_fields': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print(self.instance.id)
        self.fields['answer_fields'].label = self.instance.question_content
        self.fields['answer_fields'].queryset = self.instance.answer_fields.all()

QFormSet = forms.modelformset_factory(Question, form=QuestionForm, extra=0) 

