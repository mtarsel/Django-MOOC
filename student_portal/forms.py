from django import forms

from .models import Student

class SubmissionForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
#	fields = [ 'first_name', 'last_name', 'email', 'username']
#	exclude = ("user")
