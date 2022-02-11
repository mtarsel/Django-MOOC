THIS REPO IS OUTDATED AND UNSUPPORTED
===========

###Project name: Django Mooc: Dreaming of Teachers Incorporating Technologies

MOOC Project for Software Design and Development at Clarkson University

### Description

MOOC stands for Massive Open Online Course which is an online course aimed at unlimited participation and open access via the web. This project allows any academic institute to organize their courses and efficiently distribute course materials quickly to a large amounts of students. 

Installation
----

###Prerequisites

1. Tested with Python2.7
2. Linux 
See attached [INSTALL script](./INSTALL.sh)

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

Running the Test Server
----
You must run the test server outside of the virtualenv and execute with sudo
access. This is because of the issue with matplotlib working inside a virtualenv
The command inside the project is:

```bash

sudo python manage.py runserver
```

Registration Testing
----
To run the email server for resgistration, execute the following commands in the
directory with manage.py:

```bash

python -m smtpd -n -c DebuggingServer localhost:1025

sudo python manage.py runserver #outside of virtualenv
```

Making test objects
----
1) Follow this tutorial to make your psql work without using a password (this is obviously unsafe but this is a toy and we don't have valuable data anyway):

http://sharadchhetri.com/2013/08/17/how-to-set-user-postgres-password-in-postgresql-9-1/

2) Become the postgresuser using: sudo su postgres

3) Enter the postgresql shell using: psql

4) drop database mooc_database;

5) exit the psql shell with \q, then as postgres enter: createdb mooc_database

6) as yourself, do manage.py syncdb

7) flush your database using manage.py flush. this should redo the database and prompt you to create a new admin and whatnot

8) open the django shell (manage.py shell) and enter: from make_fake_data import make_data; make_data()

This should make a bunch of user objects, one of them is an instructor and the rest are students. 

It enrolls the students in a Django Class and adds one of each assignment type and two lectures. 

Instructions
----

1. Install all dependecies
2. Configure database and run email test server

Further Work
----

Social Authentication/Registration
Taking notes during class
Forum

---

Some help from https://code.google.com/p/classcomm/

Fake Accounts
username: admin
password: 1 
