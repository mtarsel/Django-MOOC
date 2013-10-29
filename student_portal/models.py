from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#USER:
#username
#password
#email
#first name
#last name

class Instructor(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.user)

class Course(models.Model):
    name = models.CharField(max_length=512)
    instructor = models.ForeignKey(Instructor)
    department = models.CharField(max_length=4)
    description = models.CharField(max_length=512)

    def __unicode__(self):
        return unicode(self.name)

class Student(models.Model):
    user = models.OneToOneField(User)

    course = models.ManyToManyField(Course, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

class Assignment(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=512)
    points_possible = models.IntegerField(default=100)
    

    def __unicode__(self):
        return (self.course.name + " - " + self.name)


#class Grade(models.Model):
 #   grade = models.FloatField()
    #student = models.ForeignKey(Student, primary_key=True)
#    student = models.ForeignKey(Student)

#    def __unicode__(self):
#        return unicode(self.student.user.last_name) + ', ' + unicode(self.student.user.first_name) + " enrolled in " + unicode(self.course)

class Submission(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)

    course = models.ForeignKey(Course) #unique = true)
#    grade = models.ForeignKey(Grade)
    grade = models.FloatField(null = True, blank = True)

    assignment = models.ForeignKey(Assignment)
    submitter = models.ForeignKey(Student)
#    file = ProtectedFileField(upload_to=get_grade_path, max_length=250)
    #file = models.FileField(upload_to="files/course.id/assignment.id/submission.id/user.username/%Y_%m_%d/")
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


    def get_grade_path(self, filename):
        savename = str(self.assignment.name) + os.path.splitext(filename)[1]
        return os.path.join('uploads/submitted_files/',
                            self.course.department,
                            self.course.name,
                            self.submitter.username,
                            savename)

    def __unicode__(self):
        return (self.assignment.__unicode__() + " - " + self.submitter.user.username)
