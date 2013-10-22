from django.contrib import admin
from django.utils.encoding import force_unicode

from spine.models import Grade, Course, Student, Instructor, Assignment, Submission

admin.site.register(Grade)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Course)
