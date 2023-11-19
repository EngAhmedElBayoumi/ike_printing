from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#import redirect
from django.shortcuts import redirect
#import login_required
from django.contrib.auth.decorators import login_required
from .models import ContactUs
# Create your views here.


@login_required(login_url='accounts:login')
def contact_us(request):
    if request.method=="POST":
        #get name , email , subject , message
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        #create contact us object
        contact_us = ContactUs(name=name,email=email,subject=subject,message=message)
        #save contact us object
        contact_us.save()
        #message
        messages.success(request, 'Your message has been sent successfully')
        #redirect to contact us page
        return redirect("home:home")
    return redirect("home:home")
    

    

    