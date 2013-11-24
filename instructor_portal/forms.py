from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from student_portal.models import Instructor, Course

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

class NewCourseForm(forms.ModelForm):
   
#    def __init__(self, *args, **kwargs):
#	self.request = kwargs.pop("request")
#	super(NewCourseForm, self).__init__(*args,**kwargs)
	
    class Meta:
    
	
	model = Course

	fields = ['name', 'department', 'description']
	exclude = ("instructor")

#	instructor = request.user.username
