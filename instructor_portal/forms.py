from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.admin import widgets
from django.forms.models import inlineformset_factory


from student_portal.models import Instructor, Course, Assignment

class SubmissionForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(max_length=30)

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [ 'first_name', 'last_name' ]
#	exclude = ("user")

class NewCourseForm(forms.ModelForm):
    class Meta:
	model = Course
	fields = ['name', 'department', 'description']
	exclude = ("instructor")

class NewAssignmentForm(forms.ModelForm):
    class Meta:
	model = Assignment
	fields = ['name', 'description', 'due_date','points_possible','submission_type']
	exclude = ("QUIZ", "EXAM", "HOMEWORK", "PROJECT", "SUBMISSION_TYPE_CHOICES", "course")

    def __init__(self, *args, **kwargs):
        super(NewAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].widget = widgets.AdminDateWidget()

#NewAssignmentFormSet = inlineformset_factory(Course, Assignment)

'''
NewAssignmentFormSet = inlineformset_factory(Course, Assignment)

class NewAssignmentInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(NewAssignmentInlineFormSet, self).clean()
	
	for forms in self.forms:
'''
