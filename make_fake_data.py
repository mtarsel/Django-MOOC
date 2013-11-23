from student_portal.models import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from embed_video.fields import EmbedVideoField
import datetime

def make_data():
    saver = lambda x: x.save()
    instructor_count = 1
    user_info_list = [ ('sean', '1', 'Sean', 'Lyons'),
                        ('shane', '1', 'Shane', 'daMaq'),
                        ('mick', '1', 'Mick', 'Tarsel'),
                        ('mick_', '1', 'Michael', 'Tarsel'),
                        ('derek', '1', 'Derek', 'Klatt'),
                        ('palmer', '1', 'Palmer', 'Lao'),
                        ('peter', '1', 'Peter', 'Vaillancourt'),
                        ('david', '1', 'David', 'Thegermanguy'),
                        ('liu', '1'),]

    user_list = map(lambda x: User(username=x[0], password=x[1]), user_info_list)
    
    map(lambda x: x.set_password(filter(lambda y: y[0]==x.username, user_info_list)[0][1]), user_list)
    map(saver, user_list)
    
    liu_ins = Instructor(user=filter(lambda x: x.username=='liu', user_list)[0])
    liu_ins.save()
    
    django_class = Course(name='Django Class', department='CS', description='Learning Django and Python', instructor=liu_ins)
    django_class.save()

    student_info_list = user_info_list[0:-instructor_count]
    student_user_list = user_list[0:-instructor_count]
    student_ui_ls = zip(student_info_list, student_user_list)
    student_list = map(lambda x: Student(first_name=x[0][2], last_name=x[0][3], user=x[1]), student_ui_ls)
    map(saver, student_list)
    
    map(lambda x: x.course.add(django_class), student_list)

    assignment_info = [('Exam', 'An Exam', 'This is an exam', 100),
                       ('Quiz', 'A Quiz', 'This is a quiz', 20),
                       ('Project', 'A Project', 'This is a project', 40),
                       ('Homework', 'A Homework', 'This is a homework', 5)]

    assignment_list = map(lambda x: Assignment(date=datetime.datetime.now(),
                             due_date=datetime.date(2013,12,24),
                             course=django_class,
                             name=x[1],
                             description=x[2],
                             points_possible=x[3],
                             submission_type=x[0]), assignment_info)

    map(saver, assignment_list)

    lecture_info_ls = [('Intro to Python', 'http://www.youtube.com/watch?v=oT1A1KKf0SI', django_class),
                       ('Settings and Models', 'http://www.youtube.com/watch?v=D5VlpgEVVg4', django_class)]
    lecture_ls = map(lambda x: Lecture(name=x[0],video=x[1],course=x[2]), lecture_info_ls)
    map(saver, lecture_ls)


def main():
    make_data()

if __name__ == '__main__':
    main()
