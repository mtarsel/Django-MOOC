from django import forms

from .models import Student

class SubmissionForm(forms.Form):
    file = forms.FileField()

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
	fields = [ 'first_name', 'last_name']
#	exclude = ("user")
