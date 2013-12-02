from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from student_portal.models import Instructor

class SubmissionForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(max_length=30)

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [ 'first_name', 'last_name' ]
#	exclude = ("user")
