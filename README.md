dream-girlz
===========

###Project name: dreamtitz
DREAMing of Teachers Incorporating TechnologieZ

MOOC Project for software design and development taught at Clarkson University

### Description
MOOC stands for Massive Open Online Course which is an online course aimed at unlimited participation and open access via the web. This project allows any academic institute to organize their courses and efficiently distribute course materials quickly to a large amounts of students. 


Installation
----

###Prerequisites
1. Tested with Python2.7
2. Linux 

Run INSTALL.sh as sudo

Command:

```bash
sudo ./INSTALL.sh

cd ~/software-d-and-d

source venv/bin/activate

python setup.py install #for the django-scheduler
```

This will create a directory ~/software-d-and-d

After you are in that directory, the last command will enter the virtual environment

Registration Testing
----
To run the email server for resgistration, execute the following commands in the
directory with manage.py:

```bash

python -m smtpd -n -c DebuggingServer localhost:1025

python manage.py runserver
```

Making test objects
----
1) flush your database using manage.py flush. this should prompt you to create a new admin and whatnot

2) open the django shell (manage.py shell) and enter: from make_fake_data import make_data; make_data()

This should make a bunch of user objects, one of them is an instructor and the rest are students. 

It enrolls the students in a Django Class and adds one of each assignment type and two lectures. 

Instructions
----
1. Install all dependecies and get women to use dreamtitz
2. Configure database and run email test server
3. ????????
4. Profit


Further Work
----
See attached 
[TODO file](./TODO)


---

Some help from https://code.google.com/p/classcomm/

Fake Accounts
username: admin
password: 1 
