from django import forms
from django.contrib import auth
from .models import Profile
from courses.models import VAK

class UserCreateForm(auth.forms.UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = auth.get_user_model()
        # help_texts = {
        #     'username' : 'Wymagane 150 znaków lub mniej 150. Tylko litery, cyfry oraz @/./+/-/_.',
        #     'password1' : '<ul><li>Hasło musi zawierać conajmniej 8 znaków.</li><li>Hasło nie może składać się wyłącznie z cyfr.</li></ul>',
        #     'password2' : None
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nazwa użytkownika"
        self.fields["email"].label = "Adres email"
        self.fields["password1"].label = "Hasło"
        self.fields["password2"].label = "Potwierdź hasło"


class LearningTypeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['learning_type']
        labels = {
            'learning_type' : 'Typ uczenia się'
        }


class QuestionnairyForm(forms.Form):
    label1 = '1. Jaką książkę byś wybrał?'

    CHOICES1 = [
        ('V', 'Książkę z wieloma obrazkami'),
        ('A', 'Książkę z dużą ilością tekstu'),
        ('K', 'Książkę z wyszukiwaniem słów lub z krzyżówkami')
    ]

    label2 = '2. Jeśli nie jesteś pewien, jak wymówić dany wyraz, co byś zrobił?'

    CHOICES2 = [
        ('V', 'Napisałbym go, żeby sprawdzić, czy wygląda w porządku'),
        ('A', 'Wypowiedział go na głos, żeby stwierdzić, czy brzmi dobrze'),
        ('K', 'Narysował palcem litery w powietrzu')
    ]

    label3 = '3. Stoisz w sklepie w kolejce do kasy. Co wtedy robisz?'

    CHOICES3 = [
        ('V', 'Rozglądasz się dookoła, patrząc na inne produkty w sklepie'),
        ('A', 'Rozmawiasz z osobą stojącą obok'),
        ('K', 'Poruszasz się lekko wprzód i w tył')
    ]

    label4 = '4. Kiedy widzisz słowo „samolot”, co dzieje się najpierw?'

    CHOICES4 = [
        ('V', 'Wyobrażasz sobie widok samolotu w myślach'),
        ('A', 'Wypowiadasz te słowo do samego (samej) siebie'),
        ('K', 'Myślisz o lataniu samolotem, pilotowaniem go itp.')
    ]

    label5 = '5. Jaki sposób nauki do testu jest dla Ciebie najlepszy?'

    CHOICES5 = [
        ('V', 'Czytanie książek i notatek, analizowanie obrazków i wykresów'),
        ('A', 'Poproszenie kogoś o zadawanie Ci pytań, byś mógł (mogła) na nie głośno odpowiedzieć'),
        ('K', 'Zrobienie odpowiednich zakładek, celem szybszego wyszukiwania informacji')
    ]

    label6 = '6. W jaki sposób chciał(a)byś dowiedzieć się, w jaki sposób coś działa?'

    CHOICES6 = [
        ('A', 'Poprosić kogoś, by Tobie pokazał'),
        ('V', 'Przeczytać instrukcję'),
        ('K', 'Spróbować się dowiedzieć na własną rękę')
    ]

    label7 = '7. Co Ciebie najbardziej rozprasza, gdy próbujesz się uczyć? '

    CHOICES7 = [
        ('A', 'Głośne hałasy'),
        ('K', 'Niewygodne siedzenie'),
        ('V', 'Ludzie przechodzący obok')
    ]

    label8 = '8. Kiedy jesteś szczęśliwy, co wtedy najczęściej robisz?'

    CHOICES8 = [
        ('V', 'Uśmiechasz się'),
        ('A', 'Dużo rozmawiasz'),
        ('K', 'Rozpiera Cię energia, dzięki czemu wykonujesz wiele różnych czynności')
    ]

    label9 = '9. Co robisz, gdy próbujesz się odnaleźć w nowym miejscu?'

    CHOICES9 = [
        ('V', 'Szukasz na mapie, lub patrzysz na drogowskazy'),
        ('A', 'Pytasz kogoś o drogę'),
        ('K', 'Chodzisz dookoła aż znajdziesz to, czego szukasz')
    ]

    label10 = '10. Które z tych zajęć byłyby twoimi ulubionymi?'

    CHOICES10 = [
        ('K', 'Gimnastyka'),
        ('A', 'Zajęcia muzyczne'),
        ('V', 'Koło plastyczne')
    ]

    label11 = '11. Kiedy słyszysz jakąś piosenkę, co wtedy najczęściej się zdarza?'

    CHOICES11 = [
        ('V', 'Wyobrażasz sobie teledysk do tej piosenki'),
        ('A', 'Śpiewasz lub nucisz ją'),
        ('K', 'Tańczysz do niej lub przynajmniej stukasz o coś palcami')
    ]

    label12 = '12. Co najchętniej robisz dla relaksu?'

    CHOICES12 = [
        ('A', 'Słuchasz muzyki'),
        ('V', 'Czytasz książkę'),
        ('K', 'Ćwiczysz')
    ]

    label13 = '13. W jaki sposób spróbował(a)byś zapamiętać czyjś numer telefonu?'

    CHOICES13 = [
        ('A', 'Wypowiedzieć go głośno wiele razy'),
        ('V', 'Spojrzeć na cyfry na klawiaturze, zapamiętując sekwencję ich wpisywania'),
        ('K', 'Zapisać go sobie na liście kontaktów')
    ]

    label14 = '14. Jaki rodzaj nagrody najbardziej by Tobie odpowiadał?'

    CHOICES14 = [
        ('V', 'Książka'),
        ('A', 'Płyta muzyczna'),
        ('K', 'Gra komputerowa')
    ]

    label15 = '15. Gdzie najchętniej byś się wybrał(a) z przyjaciółmi?'

    CHOICES15 = [
        ('V', 'Do kina'),
        ('A', 'Na koncert'),
        ('K', 'Do parku lub na siłownię')
    ]

    label16 = '16. Co najlepiej zapamiętujesz związku z nowopoznaną osobą?'

    CHOICES16 = [
        ('V', 'Jej twarz, ale nie imię'),
        ('A', 'Jej imię, ale nie twarz'),
        ('K', 'Temat rozmowy z tą osobą')
    ]

    label17 = '17. Jeśli miał(a)byś wskazać komuś drogę , jak byś to zrobił(a)?'

    CHOICES17 = [
        ('V', 'Opisać wygląd budynków lub innych charakterystycznych miejsc, które należy minąć, by dotrzeć do celu'),
        ('A', 'Podać nazwy ulic, którymi należałoby się poruszać'),
        ('K', '„Chodź ze mną – będzie łatwiej, jak Ci pokażę”')
    ]

    question1 = forms.ChoiceField(choices = CHOICES1, label=label1, initial='', widget=forms.RadioSelect, required=True)
    question2 = forms.ChoiceField(choices = CHOICES2, label=label2, initial='', widget=forms.RadioSelect, required=True)
    question3 = forms.ChoiceField(choices = CHOICES3, label=label3, initial='', widget=forms.RadioSelect, required=True)
    question4 = forms.ChoiceField(choices = CHOICES4, label=label4, initial='', widget=forms.RadioSelect, required=True)
    question5 = forms.ChoiceField(choices = CHOICES5, label=label5, initial='', widget=forms.RadioSelect, required=True)
    question6 = forms.ChoiceField(choices = CHOICES6, label=label6, initial='', widget=forms.RadioSelect, required=True)
    question7 = forms.ChoiceField(choices = CHOICES7, label=label7, initial='', widget=forms.RadioSelect, required=True)
    question8 = forms.ChoiceField(choices = CHOICES8, label=label8, initial='', widget=forms.RadioSelect, required=True)
    question9 = forms.ChoiceField(choices = CHOICES9, label=label9, initial='', widget=forms.RadioSelect, required=True)
    question10 = forms.ChoiceField(choices = CHOICES10, label=label10, initial='', widget=forms.RadioSelect, required=True)
    question11 = forms.ChoiceField(choices = CHOICES11, label=label11, initial='', widget=forms.RadioSelect, required=True)
    question12 = forms.ChoiceField(choices = CHOICES12, label=label12, initial='', widget=forms.RadioSelect, required=True)
    question13 = forms.ChoiceField(choices = CHOICES13, label=label13, initial='', widget=forms.RadioSelect, required=True)
    question14 = forms.ChoiceField(choices = CHOICES14, label=label14, initial='', widget=forms.RadioSelect, required=True)
    question15 = forms.ChoiceField(choices = CHOICES15, label=label15, initial='', widget=forms.RadioSelect, required=True)
    question16 = forms.ChoiceField(choices = CHOICES16, label=label16, initial='', widget=forms.RadioSelect, required=True)
    question17 = forms.ChoiceField(choices = CHOICES17, label=label17, initial='', widget=forms.RadioSelect, required=True)

    def count_points (self):
        V = 0
        A = 0
        K = 0
        for q in self.cleaned_data:
            if self.cleaned_data[q] == 'V':
                V += 1
            if self.cleaned_data[q] == 'A':
                A += 1
            if self.cleaned_data[q] == 'K':
                K += 1
            print(self.cleaned_data[q])
        print(V)
        print(A)
        print(K)
        if V > A and V > K:
            return VAK.WZROKOWIEC
        if A > V and A > K:
            return VAK.SLUCHOWIEC
        if K > A and K > V:
            return VAK.KINESTETYK

        
