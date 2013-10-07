from django.contrib import admin
from django.utils.encoding import force_unicode
from spine.models import *

admin.site.register(Grade)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
