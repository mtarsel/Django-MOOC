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

Configuring the Database
----
For some Linux distributions you may need to make a slight change to the pg_hba.conf
If you receive an error about "Authentication Failure" then follow the instructions below.

Set the password to pa55word

This is in mooc/settings.py

```bash
sudo apt-get install postgresql

sudo su - postgres

createuser --superuser liu

psql

\password liu

\q

createdb -U liu -O liu mooc_database

exit

python manage.py syncdb
```

If you receive an error about Peer Authentication failure, follow the steps below:

```bash
sudo vim /etc/postgresql/9.1/main/pg_hba.conf 

sudo /etc/init.d/postgresql restart
```

This with create a new user liu and a new postgresql database called mooc_database.



---

Some help from https://code.google.com/p/classcomm/

Fake Accounts
username: admin
password: 1 
