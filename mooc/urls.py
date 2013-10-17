from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', spine.views.index, name="index"),#index page
    url(r'^about/$', spine.views.about, name="about"),#information about MOOC
    url(r'^login/$', spine.views.login, name="login"),#login page
    url(r'^courses/$', spine.views.courses,name="courses"),#show all courses available
    
    url(r'^student/$', include('student.urls'), name="student"),#home page for student after login
    url(r'^instructor/$', include('instructor.urls'), name="instructor"),

# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
