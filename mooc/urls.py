from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^login/$', mooc.views.login_fields, name="login"),#login page
#    url(r'^login/next=?$', login_view),
    url(r'^student/$', mooc.views.student, name="student"),#home page for student after login
    url(r'^instructor/$', mooc.views.instructor_view, name="instructor"),
#    url(r'^course/{/s}/files$', file_upload),
#    url(r'^course/files/$', file_upload),
# Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
