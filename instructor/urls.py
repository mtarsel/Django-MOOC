from django.conf.urls import patterns, include, url

urlpatterns = patterns( '', 
        ( r'^home/$', instructor.views.home, name="instructor-home" ),#/instructor/home for instructor dashboard
        ( r'^courses/$', instructor.views.courses, name="instructor-courses" ),#/instructor/courses a list of all courses instructor is enrolled in
)
