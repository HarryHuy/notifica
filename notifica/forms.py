from django import forms
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ObjectDoesNotExist
from .models import Organization, ExtendedUser


UserModel = ExtendedUser


class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
            max_length=30,
            required=False,
            initial=self.user.first_name,
            widget=forms.TextInput(attrs={
                'placeholder': 'First Name',
            }))

        self.fields['last_name'] = forms.CharField(
            max_length=30,
            required=False,
            initial=self.user.last_name,
            widget=forms.TextInput(attrs={
                'placeholder': 'Last Name',
            }))


class OrgForm(forms.Form):
    name = forms.ModelChoiceField(
        required=False,
        queryset=Organization.objects.all(),
    )


class BaseOrgFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                if name != '':
                    try:
                        Organization.objects.get(name=name)
                    except ObjectDoesNotExist:
                        raise forms.ValidationError(
                            'Organization does not exist!',
                            code='org_does_not_exist'
                        )
