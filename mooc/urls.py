from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from mooc.views import index, about, display_course_info, select_login
from student_portal.views import *

urlpatterns = patterns('',
    
    #DEFAULT ADMIN VIEW
    url(r'^admin/', include(admin.site.urls)),
    
    #VIEWS IN MOOC/VIEWS.PY
    url(r'^$', index, name="index"),#index page
    url(r'^about/$', about, name="about"),#information about MOOC
    url(r'^login/$', select_login, name="select_login"),#select either student or instructor to login as
    url(r'^courses/$', enroll_courses,name="courses"),#show all courses available

    # student portal.
    url(r'^student/', include('student_portal.urls', namespace="student"), name="student"),

    # instructor portal.
    url(r'^instructor/', include('instructor_portal.urls', namespace="instructor")),
    
    #django shcedulers app for calendar
    url(r'^schedule/', include('schedule.urls')),
    
    #File upload
    url(r'^$', RedirectView.as_view(url='/student/list/')), # Just for ease of use   
 
    # django registration simple, no email registration
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # your custom registration view
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),

    # course info display
    url(r'^courses/(\d+)/$', display_course_info, name='display_course_info'),
)
