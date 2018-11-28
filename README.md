Planit
=================================================
Planit is a task tracker, dinner planner, and weather checker web application.
The application requires registration and login, and has a password rest feature.
Users are also able to edit their account settings.
If yoou have appointments for the day yoou will recieve an email at 5:00am UTC, reminding you of the appointments.
When you create or edit a dinner plan you will also recieve an email with a copy of your dinner plan.
All emails are handled via Celery and RabbitMQ.
There is also a periodic task schedule running with Celery, this can be managed from the command line or from the Django admin interface.

This project relies on the following technologies:
==================================================
* Python 3
* Django 2
* Celery 3.1.25 (django-celery, and django-celery-email 1.1.5)
* RabbitMQ
* JQuery 3.3.1
* Bootstrap 4 (CDN)
* Font Awesome (CDN)
* html5
* css3

NOTE:
---------------------------------------------------------------------------------------------------------------------
Python is required to run and use this project as a developer.
If you are using a Linux distro or a Mac you will need to put the project into a python 3 virtualenv as Python 2.7 (comes with all Linux and Apple computers, and is the default) might cause unexpected behaviour.
On Windows a virtualenv is not required but is recommended.
---------------------------------------------------------------------------------------------------------------------
BACKGROUND IMAGE:
------------------
The background image seen on pages prior to login comes from https://www.pexels.com/
The license of the image allows for personal and commercial use without attribution.
see pexels licensing information: https://www.pexels.com/photo-license/

To download the packages using pip:
-----------------------------------
*To download Django:
pip install django
Django documentation: https://docs.djangoproject.com/en/2.1/

*Install requests:
pip install request
This module is needed for the weather feature as it uses a REST API, and requires 'requests'.

To download Celery:
--------------------
Note to Windows users, support for Windows was dropped for celery V4.0 and upwards, use V3.1.25 if on Windows.
See Celery documentation on working with django. http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
Django-Celery is required if you want to manage periodic tasks from the django admin. Django-Celery and Django-Celery-Email have dependency issues with the latest version of Celery, the best combination is Django-Celery 3.1.25, and Django-Celery-Email 1.1.5. 

pip install django-celery
pip install celery==3.1.25 (Over rides the version downloaded with django-celery).
pip install django-celery-email==1.1.5

To work with celery you will need to have a message broker (RabbitMQ in this case) set up, and the email backend needs to be set up with your host email address and password.

To download RabbitMQ:
---------------------
RabbitMQ is the message broker I am using, Redis could also be used, however the broker settings in settings.py will need to be adjusted.
The download for rabbitMQ is system dependent, see the following link: https://www.rabbitmq.com/download.html
RabbitMQ will be enabled as soon as it's installed.(It will always be running as a daemon task, regardless of computer restarts)

Database:
---------
Setting up a database other than sqlite3 is sopecific to the database management sytem you choose, 
django supports both SQL and no-SQL databases.
Once you run python manage.py makemigrations, and sqlite3 database will be initialised in your project.
If you set it up like this initially and then decide to change to a RDBMS, delete all migrations and delete the sqlite3 file, set up database backends (settings.py) for the database management system you want to use and then run python manage.py makemigrations, python manage.py migrate, python manage.py createsuperuser. 
https://docs.djangoproject.com/en/2.1/ref/databases/

Thank you.
