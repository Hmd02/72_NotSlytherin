from django import forms
from django.forms import ModelForm
from .models import Test

class TestForm(ModelForm):
    
    class Meta:
        model = Test
        fields = ('image1','sub2')
