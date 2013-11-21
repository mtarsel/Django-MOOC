from django.contrib import admin
from django.utils.encoding import force_unicode

#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth import get_user_model


from student_portal.models import Course, Student, Instructor, Assignment, Submission, Lecture, Quiz, Exam, Homework, Project

#class StudentProfileInline(admin.StackedInline):
#    model = Student
#    can_delete = False

#class StudentProfileAdmin(UserAdmin):
#    inlines=(StudentProfileInline, )

admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Submission)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Exam)
admin.site.register(Homework)
admin.site.register(Assignment)
admin.site.register(Project)
#admin.site.unregister(get_user_model())
#admin.site.register(get_user_model(), StudentProfileAdmin)

