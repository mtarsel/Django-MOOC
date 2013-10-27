from django import forms

#class UploadFileForm(forms.Form):
#   title = forms.CharField(max_length=50)
#    file  = forms.FileField()

class SubmissionForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
