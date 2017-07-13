from django import forms

class UpdateUserForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')