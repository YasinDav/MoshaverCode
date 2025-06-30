from django import forms

RangeChoice = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


class ConsultFormInput(forms.Form):
    type = forms.CharField(widget=forms.HiddenInput, initial="input")
    answer = forms.CharField(widget=forms.Textarea)


class ConsultFormRange(forms.Form):
    type = forms.CharField(widget=forms.HiddenInput, initial="range")
    answer = forms.ChoiceField(choices=RangeChoice, widget=forms.RadioSelect)
