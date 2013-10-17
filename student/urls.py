from django.conf.urls import patterns, include, url

urlpatterns = patterns( '', 
        ( r'^home/$', student.views.home, name="student-home" ),#/student/home for student dashboard
        ( r'^courses/$', student.views.courses, name="student-courses" ),#/student/courses a list of all courses student is enrolled in
)
