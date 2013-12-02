from django.conf.urls import *
from instructor_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('instructor_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),

    url(r'^schedule/$', include('schedule.urls')),

    #about page
    url(r'^about/$', instructor_about, name='instructor_about'),    

    url(r'^courses/$', 'display_courses', name='display_courses'),#show all courses available    

    #edit instructor profile 
    url(r'^edit_profile/$', auth(InstructorProfileEditView.as_view()), name="edit_profile"),

    # course_info for instructors
    url(r'^([A-Z|a-z]{2,4})/(\d+)/$', display_course_info, name='display_course_info'),

    #instructor course dashboards
    url(r'^(\d+)/dashboard/$', 'course_dashboard', name='course_dashboard'),

<<<<<<< HEAD
    url(r'^(\d+)/assignments/(\d+)/$', 'assignment_dashboard', name='assignment_dashboard'),
    url(r'^(\d+)/assignments/(\d+)/(\d+)/download/$', 'download_submission', name=download_submission),
    
    #View All Student Grades for a course
    url(r'^(\d+)/dashboard/grades', 'course_grades', name='course_grades'),
=======
    #upload course material
    url(r'^(\d+)/upload_course_material/$', upload_course_material, name='upload_course_material'),

    #download course material
    url(r'^(\d+)/download_course_material/(\d+)/$', download_course_material, name='download_course_material'),

    #delete course material
    url(r'^(\d+)/delete_course_material/(\d+)/$', delete_course_material, name='delete_course_material'),

    url(r'^(\d+)/assignments/(\d+)/$', assignment_dashboard, name='assignment_dashboard'),
    url(r'^(\d+)/assignments/(\d+)/(\d+)/download/$', download_submission, name='download_submission'),
>>>>>>> e7e9b7292e53a2c7e0ae0a8c4c68473cbc6e2aea
)
