from django.conf.urls import *
from instructor_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('instructor_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),
    
    #List uploaded files
    url(r'^list/$', 'list', name='list'),

    #edit instructor profile 
#    url(r'^edit_profile/$', auth(InstructorProfileEditView.as_view()), name="edit_profile"),

# create course page
    url(r'^new-course/', create_course, name='create_course'),

)
