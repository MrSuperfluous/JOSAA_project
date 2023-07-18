from django import forms
from .models import *
ROUND_CHOICES = [
    (1, 'Round 1'),
    (2, 'Round 2'),
    (3, 'Round 3'),
    (4, 'Round 4'),
    (5, 'Round 5'),
    (6, 'Round 6'),
]

YEAR_CHOICES = [
    (2016, '2016'),
    (2017, '2017'),
    (2018, '2018'),
    (2019, '2019'),
    (2020, '2020'),
    (2021, '2021'),
    (2022, '2022'),

]
class Choices_form(forms.Form):
    insti = forms.ModelChoiceField(queryset=Institute.objects.all(),required=False)
    acad =  forms.CharField(widget=forms.HiddenInput(), required=False)
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(),required=False)
    seat = forms.ModelChoiceField(queryset=SeatType.objects.all(),required=False)
    round_no = forms.ChoiceField(choices= ROUND_CHOICES,required=False)
    year = forms.ChoiceField(choices =YEAR_CHOICES,required=False)
    
class Branch_form(forms.Form):
     insti = forms.ModelChoiceField(queryset=Institute.objects.all(),required=False)  
