from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
# read up on documentation on flash messaging in platform (django-model validations)
from time import gmtime, strftime, strptime
from .. users_app.models import User
from models import *
import time
import datetime


# Create your views here.
def index(request):
    print "User is now viewing appointments!"
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'current_date': datetime.datetime.now().strftime('%a %b %d, %Y'),
        'today_appt': Appointment.objects.filter(date=datetime.datetime.now().date()).order_by("time"),
        'future_appt': Appointment.objects.exclude(date=datetime.datetime.now().date()).order_by("date")
    }
    return render(request, "appointments_app/index.html", context)

def add_process(request):
    appointment = Appointment.objects.appoint_validator(request.POST)

    if type(appointment) == list:
        for error in appointment:
            messages.error(request, error)
        return redirect('/appointments')

    # if no errors to print run this...
    messages.success(request, "Sucessfully added the appointment!")
    return redirect('/appointments')

def edit_process(request, num):
    if request.method == 'POST':
        appointment = Appointment.objects.edit_validator(request.POST, num)

        if type(appointment) == list:
            for error in appointment:
                messages.error(request, error)
            return redirect('/appointments')

        # if no errors to print run this...
        messages.success(request, "Sucessfully edited the appointment!")
        return redirect('/appointments')
    else:
        time = Appointment.objects.get(id=num).time
        context = {
            "current_apt": Appointment.objects.get(id=num),
            "current_date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "current_time": time.strftime('%H:%M')
        }
        return render(request, "appointments_app/edit.html", context)

def delete(request, num):
    Appointment.objects.get(id=num).delete()
    messages.success(request, "Successfully deleted the appointment!")
    return redirect('/appointments')