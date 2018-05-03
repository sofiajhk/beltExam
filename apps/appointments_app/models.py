from __future__ import unicode_literals
from django.db import models
from ..users_app.models import User
from time import gmtime, strftime
import datetime
import re
import bcrypt

# Create your models here.
class AppointmentManager(models.Manager):
    # basic validation for adding appointments
    def appoint_validator(self, postData):
        date_format = "%Y-%m-%d"
        # '%Y-%m-%d %H:%M:%S+%:z'.strftime('%Y-%m-%d')
        appointment_date = datetime.datetime.strptime(postData['date'], date_format).date()
        current_date = datetime.datetime.now().date()
        errors = []
        
        if len(postData['date']) == 0 or len(postData['time']) == 0:
            # if date is not provide and follows mm/dd/yyyy format...
            errors.append("You must provide a valid date and time!")
        elif appointment_date < current_date:
            errors.append("You must provide a current or future date!")

        if Appointment.objects.filter(date=postData['date']).count() > 0 and Appointment.objects.filter(time=postData['time']).count() > 0:
            errors.append("You already have an appointment at this time!")

        if len(postData['tasks']) == 0:
            errors.append("You must provide a task!")

        if errors:
            return errors
        else:
            # if no errors, return appointment
            new_appt = self.create(
                task = postData['tasks'],
                date = appointment_date,
                time = postData['time'],
            )
            return new_appt
    
    def edit_validator(self, postData, num):
        date_format = "%Y-%m-%d"
        appointment_date = datetime.datetime.strptime(postData['date'], date_format).date()
        # '%Y-%m-%d %H:%M:%S+%:z'.strftime('%Y-%m-%d')
        current_date = datetime.datetime.now().date()
        errors = []


        if len(postData['date']) < 10 or len(postData['time']) == 0:
            # if date is not provide and follows mm/dd/yyyy format...
            errors.append("You must provide a valid date and time!")
        elif appointment_date < current_date:
            errors.append("You must provide a current or future date!")

        if postData['status'] == "Pending" and len(Appointment.objects.filter(date=postData['date'])) > 0 and len(Appointment.objects.filter(time=postData['time'])) > 0:
            errors.append("You already have an appointment at this time!")

        if len(postData['tasks']) == 0:
            errors.append("You must provide a task!")

        if len(postData['status']) == 0:
            errors.append("You must provide a status!")

        if errors:
            return errors
        else: 
            edit = self.get(id=num)
            edit.task = postData['tasks']
            edit.date = appointment_date
            edit.time = postData['time']
            edit.status = postData['status']
            edit.save()
            return edit 

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateTimeField()
    time = models.TimeField()
    status = models.CharField(max_length=255, default="Pending")
    # OneToMany relationship with User / define relationship in Appointment because it's on Many side of relatioinship
    user = models.ManyToManyField(User, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<User object: Task: {} \nTime: {} \nDate: {} \nStatus: {} \nCreated: {} \nUpdated: {}>".format(self.task, self.time, self.date, self.status, self.created_at, self.updated_at)

    objects = AppointmentManager()


        