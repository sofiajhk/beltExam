from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from models import *
import time
import datetime

# Create your views here.
def index(request):
    print "someone is logging-in or registering"
    # context = {
    #     'Users': User.objects.all()
    # }
    return render(request, "users_app/index.html") #, context)

def success(request):
    print "User succesfully registered/signed in!"
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "users_app/success.html", context)

def reg_process(request):
    result = User.objects.register_validator(request.POST)
    print result

    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    
    # if no errors to print run this...
    request.session['user_id'] = result.id
    messages.success(request, "Sucessfully registered!")
    return redirect('/success')


def log_process(request):
    result = User.objects.login_validator(request.POST)
    print result
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    
    # if no errors to print run this...
    request.session['user_id'] = result.id
    messages.success(request, "Succesfully logged in!")
    return redirect('/success')

def logout(request):
    del request.session['user_id']
    print "User succesfully logged out!"
    messages.success(request, "Goodbye! See you next time!")
    return redirect('/')
