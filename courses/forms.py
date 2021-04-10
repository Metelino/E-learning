from django import forms
from .models import Course, Node, LessonFile, Question, Answer

class CourseForm(forms.ModelForm):
    class Meta():
        model = Course
        fields = ['name', 'desc']
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
        fields = ['name', 'desc']
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
        fields = ['name', 'desc', 'node_type']
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
        fields = ['name', 'desc']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
        }
        widgets = {
            'name' : forms.TextInput(attrs = {'class' : 'input'}),
            'desc': forms.Textarea(attrs={'rows': 10, 'class':'textarea', 'style':'resize:none;'}),
        }

class FileForm(forms.ModelForm):
    class Meta():
        model = LessonFile
        fields = ['lesson_type', 'lesson_file']
        # widgets = {
        #     # 'lesson_type' : forms.HiddenInput(),
        #     #'lesson_file' : forms.FileInput(attrs = {'class':"file-input"})
        # }
        labels = {
            'lesson_file' : 'Plik',
            'lesson_type' : 'Typ uczenia się',
        }

FileFormSet = forms.formset_factory(FileForm, extra=0)

class QCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': 'Treść pytania'}
        widgets = {
            'text' : forms.TextInput(attrs = {'class':'input'}),
        }

class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']
        widgets = {
            'text' : forms.TextInput(attrs = {'class':'input', 'style':'display:inline-block;'}),
        }
        labels = {
            'text' : '',
            'correct' : ''
        }

AnswerCreateFormSet = forms.modelformset_factory(Answer, extra=2, form=AnswerCreateForm)
#AnswerCreateFormSet = forms.modelformset_factory(Answer, extra=2, fields=['text','correct'])

class QuestionEditForm(forms.ModelForm):
    model = Question

class QuestionForm(forms.ModelForm):
    class Meta():
        model = Question
        fields = ['answers']
        widgets = {'answers': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answers'].label = self.instance.text
        self.fields['answers'].queryset = self.instance.answers.all()
        self.fields['answers'].initial = Answer.objects.none()
        
        #print(self.instance.id)
        

    def check_answers(self):
        correct = self.instance.answers.filter(correct=True)
        print(correct)
        print(self.cleaned_data['answers'])
        return set(self.cleaned_data['answers']) == set(correct)
        


QFormSet = forms.modelformset_factory(Question, form=QuestionForm, extra=0) 
#AnswerFormSet = forms.modelformset_factory(Answer, extra=0, fields=['text'])
