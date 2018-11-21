Planit
=================================================
Planit is a task tracker, dinner planner, and weather checker web application.
The application requires registration and login, and has a password rest feature.
Users are also able to edit their account settings.
All emails are handled via Celery and RabbitMQ.

This project relies on the following technologies:
==================================================
* Python 3
* Django 2
* celery (django-celery, and django-celery-email)
* rabbitMQ
* JQuery 3.3.1
* Jquery UI
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

To download the packages using pip:
-----------------------------------
To download django:
pip install django

To download celery:
* Note to Windows users, support for Windows was dropped for celery V4.0 and upwards, use V3.1.25 if on Windows.
pip install django-celery
pip install django-celery-email

*To download rabbitMQ:
*The download for rabbitMQ is system dependent, see the following link: https://www.rabbitmq.com/download.html

To work with celery you will need to have the email backend set up with your host email address and password.

Setting up a database other than sqlite3 is sopecific to the database management sytem you choose, 
django supports both SQL and no-SQL databases.

Thank you.
