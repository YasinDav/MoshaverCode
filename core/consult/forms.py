from django import forms

RangeChoice = [
    ('very good', 'very good'),
    ('good', 'good'),
    ('normal', 'normal'),
    ('bad', 'bad'),
    ('very bad', 'very bad'),
]


class ConsultFormInput(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)


class ConsultFormRange(forms.Form):
    answer = forms.ChoiceField(choices=RangeChoice, widget=forms.RadioSelect)
