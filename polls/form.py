from django import forms

class  formed(forms.Form):
    name=forms.CharField(label='Enter your text',widget=forms.Textarea(attrs={'class':'form-control border-dark float-left'}),required=False)
    url=forms.CharField(label='Enter your url',widget=forms.TextInput(attrs={'class':'form-control border-dark float-left'}),required=False)
