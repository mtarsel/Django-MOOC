from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from spine.views import index, about, courses #,login, register

urlpatterns = patterns('',
    url(r'^$', index, name="index"),#index page
    url(r'^about/$', about, name="about"),#information about MOOC
#    url(r'^login/$', login, name="login"),#login page for instructor and students
#    url(r'^register/$', register, name="register"),#register page for new users
    url(r'^courses/$', courses,name="courses"),#show all courses available
    
    url(r'^student/', include('student.urls')),#dashboard for student after login
    url(r'^instructor/', include('instructor.urls')),#dashboard for instructor after login

    url(r'^accounts/', include('registration.backends.simple.urls')),

#    url(r'^accounts/', include('registration.backends.default.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
