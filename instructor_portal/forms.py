from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from student_portal.models import Instructor

class SubmissionForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [ 'first_name', 'last_name' ]
#	exclude = ("user")
