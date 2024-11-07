from django import forms

class AddNewItemForm(forms.Form):
    url = forms.CharField(max_length=600)