from __future__ import absolute_import
import datetime
from celery import Celery
from django.core.mail import send_mail
#from celery.schedules import crontab
from django.template import loader
from .models import TodoList


app = Celery('tasks', broker='amqp://guest:guest@localhost:5672/')
app.config_from_object('dinner_planner.settings')


@app.task
def plan_email(monday, tuesday, wednesday, thursday, friday, saturday, sunday, user):
    ctx = {
        'Monday': monday,
        'Tuesday': tuesday,
        'Wednesday': wednesday,
        'Thursday': thursday,
        'Friday': friday, 
        'Saturday': saturday,
        'Sunday': sunday
    }
    subject = 'Dinner plan for the week'
    content = loader.get_template('planner/email_plan.txt').render(ctx)
    from_email = 'django.testacc306@gmail.com'
    to = [user]
    send_mail(
        subject,
        content,
        from_email,
        to,
        fail_silently = False,
    )


@app.task
def contact_email(name, message, email):
    ctx = {
        'Name': name,
        'Message': message,
        'Email': email
    }
    subject = 'A user has contacted us.'
    content = loader.get_template('planner/contact.txt').render(ctx)
    from_email = 'django.testacc306@gmail.com'
    to = ['stuartsargent208@gmail.com']
    send_mail(
        subject,
        content,
        from_email,
        to,
        fail_silently = False,
    )


@app.task
def email_reminder():
    reminders = TodoList.objects.filter(Due=datetime.date.today())
    for reminder in reminders:
        subject = reminder.Task
        content = reminder.Info
        from_email = 'django.testacc306@gmail.com'
        to = [str(reminder.User)]
        send_mail(
            subject,
            content,
            from_email,
            to,
            fail_silently = False,
        )





