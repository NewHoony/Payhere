from django import forms
from django.forms.widgets import TextInput
from django.core.validators import MinValueValidator
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['memo', 'money', 'receipt']