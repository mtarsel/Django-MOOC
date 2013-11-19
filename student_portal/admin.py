from django.contrib import admin
from django.utils.encoding import force_unicode

from student_portal.models import Course, Student, Instructor, Assignment, Submission, Lecture, Quiz, Exam, Homework

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Submission)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Exam)
admin.site.register(Homework)
admin.site.register(Assignment)
