from django import forms
from django.contrib.auth.models import User


class Auth_codeForm(forms.Form):
    code = forms.IntegerField(label="Код регистрации")


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
