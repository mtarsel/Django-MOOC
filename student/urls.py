from django.conf.urls import patterns, include, url

from student.views import home, courses

urlpatterns = patterns( 'mooc.student', 
#    url(r'^$', index, name="index"),#index page    
    url(r'^$', home, name="student-home" ),#/student/home for student dashboard
    url(r'^courses/$', courses, name="student-courses" ),#/student/courses a list of all courses student is enrolled in
)
