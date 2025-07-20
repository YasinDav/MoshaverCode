from django import forms

RangeChoice = [
    ('very much', 'خیلی خوب'),
    ('very', 'خوب'),
    ('neutral', 'معمولی'),
    ('bad', 'بد'),
    ('very bad', 'خیلی بد'),
]


class ConsultFormInput(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control mb-2',
            'placeholder': 'لطفا اینجا بمویسید...',
            "rows": 4
        })
    )


class ConsultFormRange(forms.Form):
    answer = forms.ChoiceField(choices=RangeChoice, widget=forms.RadioSelect)
