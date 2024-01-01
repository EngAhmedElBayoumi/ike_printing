from django.contrib import messages
from django.shortcuts import render
from django.conf import settings 
from django.urls import reverse 
import uuid 
from datetime import datetime
from paypal.standard.forms import PayPalPaymentsForm 
from dragon.models import working_setting as dragon_working_setting , meeting as dragon_meeting 
from senior_dragon.models import working_setting as senior_dragon_working_setting , meeting as senior_dragon_meeting
from unicorn.models import working_setting as unicorn_working_setting , meeting as unicorn_meeting
from senior_unicorn.models import working_setting as senior_unicorn_working_setting , meeting as senior_unicorn_meeting
#import messages
from django.contrib import messages
#import zoom
# from zoomus import ZoomClient
#import settings
from django.conf import settings
#import redirect
from django.shortcuts import redirect
#import json
import json
# Create your views here.


import os

allowed_extiontion=[
    '.pdf',
    '.doc',
    '.docx',
    '.png',
    '.jpg',
    '.jpeg',
]

def allowed_file(file_name):
    #get file name 
    file_name=file_name.name
    #get file extention
    ext=os.path.splitext(file_name)[1]    
    if ext.lower() in allowed_extiontion:
        return True
    else:
        return False
    

def call_expert(request):
    return render(request, 'ChooseDesigner.html', {})


#CallSeniorDesigner
def call_senior_designer(request):
    if request.method == 'POST':
        name=request.POST.get('name') or None
        email=request.POST.get('email') or None
        subject=request.POST.get('subject') or None
        message=request.POST.get('message') or None
        fromtime=request.POST.get('fromtime') or None
        totime=request.POST.get('totime') or None
        date=request.POST.get('data') or None
        upload_file=request.FILES.get('upload_file') or None
        
        #validate all fields
        if not name or not email or not subject or not message or not fromtime or not totime or not date or not upload_file:
            messages.error(request, "All fields are required.")
            return render(request, 'CallSeniorDesigner.html', {})
        
        #check if file is empty
        if upload_file:
            #validate file type
            if not allowed_file(upload_file):
                messages.error(request, "File type not supported.")
                return render(request, 'CallSeniorDesigner.html', {})  
        
        #convert fromtime from string to time not datetime
        fromtime = datetime.strptime(fromtime, '%H:%M').time()
        #convert totime from string to time not datetime
        totime = datetime.strptime(totime, '%H:%M').time()
        date = datetime.strptime(date, '%Y-%m-%d').date()        
        #set meeting to senior dragon or senior unicorn if the time is available in senior unicorn or senior dragon
        #get all senior dragon meetings 
        unicorn_conflict = senior_unicorn_meeting.objects.filter(meeting_date=date, start_time__lte=totime, end_time__gte=fromtime).exists()
        
        check = senior_unicorn_working_setting.objects.filter(day=date.strftime("%A")).first()
        if check:
            #get break time from working day to unicorn team
            break_time_from = senior_unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
            break_time_to = senior_unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
            #check if time is in break time
            if fromtime >= break_time_from and totime <= break_time_to:
                #conflict true
                unicorn_conflict = True
        else:
            unicorn_conflict = True
        #check if the time is not exist in senior unicorn meetings add meeting to senior unicorn else check in senior dragon meetings 
        if not unicorn_conflict:
            # No conflict: schedule with senior unicorn
            # senior_unicorn_meeting.objects.create(
            #     user_name=name,
            #     user_email=email,
            #     subject=subject,
            #     message=message,
            #     meeting_date=date,
            #     start_time=fromtime,
            #     end_time=totime
            # )
            request.session['meeting_type'] = 'senior_unicorn'
            price=senior_unicorn_working_setting.objects.first().meeting_price
            #the all data of meeting on session
            request.session['meeting_data'] = {
                'user_name': name,
                'user_email': email,
                'subject': subject,
                'message': message,
                'meeting_date': date.strftime('%Y-%m-%d'),  
                'start_time': fromtime.strftime('%H:%M'),
                'end_time': totime.strftime('%H:%M'),
                'price': price
            }
            #redirect to payment
            return redirect('call_expert:redirect_to_payment')                  

            
        else:
            # Check availability in senior dragon meetings
            dragon_conflict = senior_dragon_meeting.objects.filter(meeting_date=date, start_time__lte=totime, end_time__gte=fromtime).exists()
            #get break time from working day to dragon team
            break_time_from = senior_dragon_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
            break_time_to = senior_dragon_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
            #check if time is in break time
            if fromtime >= break_time_from and totime <= break_time_to:
                #conflict true
                dragon_conflict = True

            if not dragon_conflict:
                # No conflict: schedule with senior dragon
                # senior_dragon_meeting.objects.create(
                #     user_name=name,
                #     user_email=email,
                #     subject=subject,
                #     message=message,
                #     meeting_date=date,
                #     start_time=fromtime,
                #     end_time=totime
                # )
                request.session['meeting_type'] = 'senior_dragon'
                price = senior_dragon_working_setting.objects.first().meeting_price
                #the all data of meeting on session
                request.session['meeting_data'] = {
                    'user_name': name,
                    'user_email': email,
                    'subject': subject,
                    'message': message,
                    'meeting_date': date.strftime('%Y-%m-%d'),  
                    'start_time': fromtime.strftime('%H:%M'),
                    'end_time': totime.strftime('%H:%M'),
                    'price': price
                }
                #redirect to payment
                return redirect('call_expert:redirect_to_payment')
            else:
                messages.error(request, "Sorry there is no aviailable meeting time")  
     
    return render(request, 'CallSeniorDesigner.html', {})



#call designer 6$ 
def call_designer(request):
    #get price from unicorn_working_setting if not found get price from dragon_working_setting
    #get price from unicorn_working_setting
    unicorn_price = unicorn_working_setting.objects.first()
    if unicorn_price:
        price = unicorn_price.meeting_price
    else:
        #get price from dragon_working_setting
        dragon_price = dragon_working_setting.objects.first()
        if dragon_price:
            price = dragon_price.meeting_price
        else:
            price = 6
        # Render Form 
      
    if request.method == 'POST':
        name=request.POST.get('name') or None
        email=request.POST.get('email') or None
        subject=request.POST.get('subject') or None
        message=request.POST.get('message') or None
        fromtime=request.POST.get('fromtime') or None
        totime=request.POST.get('totime') or None
        date=request.POST.get('data') or None
        upload_file=request.FILES.get('upload_file') or None
        
        #validate all fields
        if not name or not email or not subject or not message or not fromtime or not totime or not date or not upload_file:
            messages.error(request, "All fields are required.")
            return render(request, 'CallSeniorDesigner.html', {})
        
        #check if file is empty
        if upload_file:
            #validate file type
            if not allowed_file(upload_file):
                messages.error(request, "File type not supported.")
                return render(request, 'CallSeniorDesigner.html', {})  
        
        #convert fromtime from string to time not datetime
        fromtime = datetime.strptime(fromtime, '%H:%M').time()
        #convert totime from string to time not datetime
        totime = datetime.strptime(totime, '%H:%M').time()
        date = datetime.strptime(date, '%Y-%m-%d').date()
        #get all senior dragon meetings 
        unicorn_conflict = unicorn_meeting.objects.filter(meeting_date=date, start_time__lt=totime, end_time__gt=fromtime).exists()        
        
        #get break time from working day to unicorn team
        check=unicorn_working_setting.objects.filter(day=date.strftime("%A")).first()
        if check:
            break_time_from = unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
            break_time_to = unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
            #check if time is in break time
            if fromtime >= break_time_from and totime <= break_time_to:
                #conflict true
                unicorn_conflict = True
        else:
            unicorn_conflict = True
    # payment stage
    
        #check if the time is not exist in senior unicorn meetings add meeting to senior unicorn else check in senior dragon meetings 
        if not unicorn_conflict:
            # No conflict: schedule with senior unicorn
            # unicorn_meeting.objects.create(
            #     user_name=name,
            #     user_email=email,
            #     subject=subject,
            #     message=message,
            #     meeting_date=date,
            #     start_time=fromtime,
            #     end_time=totime,
            #     upload_file=upload_file
                
            # )
            request.session['meeting_type'] = 'unicorn'
            #the all data of meeting on session
            request.session['meeting_data'] = {
                'user_name': name,
                'user_email': email,
                'subject': subject,
                'message': message,
                'meeting_date': date.strftime('%Y-%m-%d'),  
                'start_time': fromtime.strftime('%H:%M'),
                'end_time': totime.strftime('%H:%M'),
                'price': price
            }
            #redirect to payment
            return redirect('call_expert:redirect_to_payment')

        else:
            # Check availability in senior dragon meetings
            dragon_conflict = dragon_meeting.objects.filter(meeting_date=date, start_time__lt=totime, end_time__gt=fromtime).exists()
            #get break time from working day to dragon team
            break_time_from = dragon_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
            break_time_to = dragon_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
            #check if time is in break time
            if fromtime >= break_time_from and totime <= break_time_to:
                #conflict true
                dragon_conflict = True
            
            
            if not dragon_conflict:
                # No conflict: schedule with senior dragon
                # dragon_meeting.objects(
                #     user_name=name,
                #     user_email=email,
                #     subject=subject,
                #     message=message,
                #     meeting_date=date,
                #     start_time=fromtime,
                #     end_time=totime,
                #     upload_file=upload_file
                # )
                request.session['meeting_type'] = 'dragon'
                price = dragon_working_setting.objects.first().meeting_price
                #the all data of meeting on session
                request.session['meeting_data'] = {
                    'user_name': name,
                    'user_email': email,
                    'subject': subject,
                    'message': message,
                    'meeting_date': date.strftime('%Y-%m-%d'),  
                    'start_time': fromtime.strftime('%H:%M'),
                    'end_time': totime.strftime('%H:%M'),
                    'price': price
                }
                #redirect to payment
                return redirect('call_expert:redirect_to_payment')
            

            else:
                messages.error(request, "No available slots with either  Unicorn or Dragon teams.")  
      
        
    return render(request, 'callEpertTwo.html')



def redirect_to_payment(request):
    #get price from session
    price = request.session['meeting_data']['price']
    print(price)
    
    host = request.get_host() # Host 
    paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER, 
            'amount' : price, 
            'item_name' : 'Fast Design Reservation', 
            'invoice' : uuid.uuid4(), 
            'currency' : 'USD', 
            'notify_url' : f'http://{host}{reverse("paypal-ipn")}/',
            'return_url' : f'http://{host}{reverse("call_expert:payment_success")}/',
            'cancel_url' : f'http://{host}{reverse("call_expert:payment_failed")}/',
    }
    paypal = PayPalPaymentsForm(initial=paypal_checkout)
    return render(request, 'order_redirect.html',{'paypal':paypal})



def payment_success(request):
    #check meeting_type 
    meeting_type = request.session['meeting_type']
    #get meeting_data
    meeting_data = request.session['meeting_data']
    #check meeting_type and save meeting
    if meeting_type == 'dragon':
        dragon_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
        )
    elif meeting_type == 'unicorn':
        unicorn_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
        )
    elif meeting_type == 'senior_dragon':
        senior_dragon_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time']
        )
    elif meeting_type == 'senior_unicorn':
        senior_unicorn_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time']
        )
    #clear session
    request.session['meeting_type'] = None
    request.session['meeting_data'] = None
    messages.success(request, "Your payment is done successfully and your meeting is scheduled.")
    return redirect('call_expert:call_expert')



def payment_failed(request):
    #clear session
    request.session['meeting_type'] = None
    request.session['meeting_data'] = None
    messages.error(request, "Your payment is failed.")
    return redirect('call_expert:call_expert')