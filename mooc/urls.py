from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from mooc.views import index, about, select_login, redirect_to_correct_dash, edit_profile, schedule
from student_portal.views import *

urlpatterns = patterns('',
    #dashboard
    url(r'^dashboard/', redirect_to_correct_dash, name="redir_dash"),
    
    #DEFAULT ADMIN VIEW
    url(r'^admin/', include(admin.site.urls)),
    
    #VIEWS IN MOOC/VIEWS.PY
    url(r'^$', index, name="index"),#index page
    url(r'^about/$', about, name="about"),#information about MOOC
    url(r'^login/$', select_login, name="select_login"),#select either student or instructor to login as
    url(r'^courses/$', enroll_courses,name="courses"),#show all courses available
    url(r'^edit_profile/$', edit_profile, name="edit_profile"),
    url(r'^schedule/$', schedule, name="schedule"),
    
    # student portal.
    url(r'^student/', include('student_portal.urls', namespace="student"), name="student"),

    # instructor portal.
    url(r'^instructor/', include('instructor_portal.urls', namespace="instructor")),
    
    #django shcedulers app for calendar
#    url(r'^schedule/', include('schedule.urls')),
    
    #File upload
    url(r'^$', RedirectView.as_view(url='/student/list/')), # Just for ease of use   
 
    # django registration simple, no email registration

#    url(r'^accounts/', include('registration.backends.simple.urls')),
    
    url(r'^accounts/',include('registration.backends.default.urls')),

    # your custom registration view
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),


)
