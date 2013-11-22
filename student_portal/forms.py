from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Student, User

class SubmissionForm(forms.Form):
    file = forms.FileField()

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'course')

    fields = [ 'first_name', 'last_name']
