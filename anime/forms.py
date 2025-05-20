from django import forms
from .models import Rating,Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widjets = {
            'value' : forms.RadioSelect(choices=[(i , str(i)) for i in range(1,6)])
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','text']
        widjets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'text':forms.Textarea(attrs={'class':'form-control', 'rows':4})
        }