from django.conf.urls.defaults import *
from student_portal.views import *

urlpatterns = patterns('student_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),
    
    #List uploaded files
    url(r'^list/$', 'list', name='list'),
)
