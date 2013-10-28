from django.contrib import admin
from django.utils.encoding import force_unicode

from student_portal.models import Course, Student, Instructor, Assignment, Submission

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Course)
