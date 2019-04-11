from django import forms

class  form1(forms.Form):
    name=forms.FileField(label='upload your file here')