from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Student

class SubmissionForm(forms.Form):
    file = forms.FileField()

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student

#	fields = [ 'first_name', 'last_name', 'email', 'username']
#	exclude = ("user")
