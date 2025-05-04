# app1/forms.py
from django import forms
from .models import app1


class app1Form(forms.ModelForm):
    class Meta:
        model = app1
        fields = ["firstName", "lastName"]
