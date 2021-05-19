from django import forms
from .models import Course, Node, LessonFile, Question, Answer, VAK
#from ckeditor.widgets import CKEditorWidget

class CourseForm(forms.ModelForm):
    class Meta():
        model = Course
        fields = ['name', 'desc', 'category']
        labels = {
            'name' : 'Tytuł kursu',
            'desc' : 'Opis kursu',
            'category' : 'Kategoria'
        }
        widgets = {
            'name' : forms.TextInput(attrs = {'class' : 'input'}),
            'desc': forms.Textarea(attrs={'rows': 10, 'class':'textarea', 'style':'resize:none;'}),
        }

class CourseSearchForm(forms.Form):
    CATEGORIES = [
        ('wszystkie', 'wszystkie'),
        ('other', 'inna'),
        ('infa', 'informatyka'),
        ('matma', 'matematyka'),
        ('fizyka', 'fizyka'),
        ('biologia', 'biologia'),
        ('chemia', 'chemia')
    ]
    name = forms.CharField(max_length=200, required=False, label='Nazwa kursu')
    category = forms.ChoiceField(choices=CATEGORIES, initial='wszystkie', label='Kategoria')
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # there's a `fields` property now
    #     self.fields['name'].required = False

    # class Meta():
    #     model = Course
    #     fields = ['name','category']
    #     labels = {
    #         'name' : 'Nazwa kursu',
    #         'category' : 'Kategoria'
    #     }

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
        fields = ['name', 'desc', 'content']
        labels = {
            'name' : 'Tytuł lekcji',
            'desc' : 'Opis lekcji',
            'content' : 'Treść lekcji'
        }
        widgets = {
            # 'desc': forms.Textarea(attrs={'rows': 10}),
            'content': forms.Textarea(attrs={'rows': 20, 'id':'editor'}),
            #'content': CKEditorWidget(),
        }
        # widgets = {
        #     'name' : forms.TextInput(attrs = {'class' : 'input'}),
        #     'desc': forms.Textarea(attrs={'rows': 10, 'class':'textarea', 'style':'resize:none;'}),
        # }

class FileForm(forms.ModelForm):
    class Meta():
        model = LessonFile
        fields = ['lesson_type', 'lesson_file']
        widgets = {
            # 'lesson_type' : forms.HiddenInput(),
            #'lesson_file' : forms.FileInput(attrs = {'class':"file-input"})
            'lesson_file' : forms.FileInput(attrs={'class':'file-input'})
        }
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
            'text' : forms.TextInput(attrs = {'class':'input', 'placeholder':"Odpowiedź"}),
            'correct': forms.CheckboxInput(attrs = {'class':'checkbox is-large'})
        }
        labels = {
            'text' : '',
            'correct' : ''
        }

AnswerCreateFormSet = forms.modelformset_factory(Answer, extra=2, form=AnswerCreateForm)
AnswerEditFormSet = forms.modelformset_factory(Answer, extra=0, form=AnswerCreateForm)
#AnswerCreateFormSet = forms.modelformset_factory(Answer, extra=2, fields=['text','correct'])

class AnswerEditForm(forms.ModelForm):
    model = Question

class QuestionForm(forms.ModelForm):
    class Meta():
        model = Question
        fields = ['answers']
        widgets = {'answers': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['answers'].label = self.instance.text
        self.fields['answers'].initial = Question.objects.none()
        self.fields['answers'].queryset = self.instance.answers
        
        print(self.fields['answers'].initial)
        #self.fields['answers'].initial = self.instance.answers.first()
        
    def check_answers(self):
        correct = self.instance.answers.filter(correct=True)
        print(correct)
        print(self.cleaned_data['answers'])
        return set(self.cleaned_data['answers']) == set(correct)
        


QFormSet = forms.modelformset_factory(Question, form=QuestionForm, extra=0) 
#AnswerFormSet = forms.modelformset_factory(Answer, extra=0, fields=['text'])
