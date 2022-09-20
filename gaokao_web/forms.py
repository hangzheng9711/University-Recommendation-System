from django import forms
from .models import PLACE_CHOICES
from .models import SUBJECT_CHOICES
from .models import LINE_CHOICES
from .models import CITY_CHOICES
from .models import PAIXU_CHOICES

class collectDataForm(forms.Form):
    score = forms.IntegerField(label="分数",min_value=100,max_value=750)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="文理分科", initial='理科')
    place = forms.ChoiceField(choices=PLACE_CHOICES, label="考生所在地", initial='重庆')

    line = forms.ChoiceField(choices=LINE_CHOICES, label="理想批次", initial=0)
    major = forms.CharField(label="理想专业", required=False)
    city = forms.ChoiceField(choices=CITY_CHOICES, label="理想城市", initial=0)

    waypaixu = forms.ChoiceField(choices=PAIXU_CHOICES, label="排序方式", initial=0)