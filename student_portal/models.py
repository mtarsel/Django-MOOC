from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from embed_video.fields import EmbedVideoField

#USER:
#username
#password
#email
#first name
#last name

class Course(models.Model):
    name = models.CharField(max_length=512)
    department = models.CharField(max_length=4)
    description = models.CharField(max_length=512)
    
    def __unicode__(self):
        return unicode(self.name)

class Instructor(models.Model):
    user = models.OneToOneField(User)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return unicode(self.user)

class Lecture(models.Model):
    name = models.CharField(max_length=20)
    video = EmbedVideoField()
    course = models.ForeignKey(Course)
    #for future feature of notes?
    #notes = models.CharField(max_length=512)
    
    def __unicode__(self):
        return (self.course.name + " - " + self.name)


class Student(models.Model):
    user = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=30)
    course = models.ManyToManyField(Course, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

class Assignment(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    due_date = models.DateTimeField(editable=True)
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=512)
    points_possible = models.IntegerField(default=100)
    QUIZ = 'Quiz'
    EXAM = 'Exam'
    HOMEWORK = 'Homework'
    PROJECT = 'Project'
    SUBMISSION_TYPE_CHOICES = (
        (QUIZ, 'Quiz'),
        (EXAM, 'Exam'),
        (HOMEWORK, 'Homework'),
        (PROJECT, 'Project'))
    submission_type = models.CharField(max_length=8,
                                       choices=SUBMISSION_TYPE_CHOICES,
                                       default=QUIZ)
    
    
    def __unicode__(self):
        return (self.course.name + " - " + self.name)


class Submission(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    course = models.ForeignKey(Course) 
    grade = models.FloatField(null = True, blank = True)
    assignment = models.ForeignKey(Assignment)
    submitter = models.ForeignKey(Student)
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

class Quiz(Submission):
    weight = .2

class Exam(Submission):
    weight = .4

class Homework(Submission):
    weight = .2

class Project(Submission):
    weight = .2
