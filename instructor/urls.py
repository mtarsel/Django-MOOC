from django.conf.urls import patterns, include, url

from instructor.views import home, courses

urlpatterns = patterns( 'mooc.instructor', 
#    url(r'^$', index, name="index"),#index page    
    url(r'^$', home, name="instructor-home" ),#/instructor/home for instructor dashboard
    url(r'^courses/$', courses, name="instructor-courses" ),#/instructor/courses a list of all courses instructor is enrolled in
)
