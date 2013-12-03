from django.conf.urls import *
from instructor_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('instructor_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),

#    url(r'^schedule/$', include('schedule.urls')),

    #about page
    url(r'^about/$', instructor_about, name='instructor_about'),    

    url(r'^courses/$', 'display_courses', name='display_courses'),#show all courses available    

    #edit instructor profile 
    url(r'^edit_profile/$', auth(InstructorProfileEditView.as_view()), name="edit_profile"),

    # create course page
    url(r'^new-course/', create_course, name='create_course'),

    # create a new assignment page
    url(r'^(\d+)/new-assignment/$', 'new_assignment'),
    
    # create a new lecture page
    url(r'^(\d+)/new-lecture/$', 'new_lecture'),

    # course_info for instructors
    url(r'^([A-Z|a-z]{2,4})/(\d+)/$', display_course_info, name='display_course_info'),

    #instructor course dashboards
    url(r'^(\d+)/dashboard/$', 'course_dashboard', name='course_dashboard'),

    url(r'^(\d+)/assignments/(\d+)/$', 'assignment_dashboard', name='assignment_dashboard'),
    url(r'^(\d+)/assignments/(\d+)/(\d+)/download/$', 'download_submission', name=download_submission),
    
    #View All Student Grades for a course
    url(r'^(\d+)/dashboard/grades', 'course_grades', name='course_grades'),
    #upload course material
    url(r'^(\d+)/upload_course_material/$', upload_course_material, name='upload_course_material'),

    #download course material
    url(r'^(\d+)/download_course_material/(\d+)/$', download_course_material, name='download_course_material'),

    #delete shit
    url(r'^(\d+)/delete_course_material/(\d+)/$', delete_course_material, name='delete_course_material'),
    url(r'^(\d+)/delete_assignment/(\d+)/$', delete_assignment, name='delete_assignment'),
    url(r'^(\d+)/delete_lecture/(\d+)/$', delete_lecture, name='delete_lecture'),
    url(r'^(\d+)/delete_course/$', delete_course, name='delete_course'),

    url(r'^(\d+)/assignments/(\d+)/$', assignment_dashboard, name='assignment_dashboard'),
    url(r'^(\d+)/assignments/(\d+)/(\d+)/download/$', download_submission, name='download_submission'),
)
