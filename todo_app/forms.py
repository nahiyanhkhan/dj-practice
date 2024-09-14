from pyexpat import model
from django import forms
from .models import Task


class SearchForm(forms.Form):
    query = forms.CharField(required=False)


class AddTodoForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    description = forms.CharField(widget=forms.TextInput)
