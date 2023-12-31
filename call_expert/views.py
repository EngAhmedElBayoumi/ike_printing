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
from zoomus import ZoomClient
#import settings
from django.conf import settings
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
    
    
def schedule_zoom_meeting(request):
    API_KEY = settings.ZOOM_API_KEY
    API_SECRET = settings.ZOOM_API_SECRET
    api_account_id = 'HauKd7KdQkqSDQaDtQA69w'
    
    # Create Zoom client
    client = ZoomClient(API_KEY, API_SECRET)
    client.user.get(id=api_account_id)    

    # Set up meeting details
    meeting_info = {
        'topic': 'Scheduled Meeting',
        'type': 2,  # Scheduled meeting
        'start_time': '2023-12-28T12:00:00Z',  # Replace with your desired start time
        'duration': 30,  # Meeting duration in minutes
    }

    # Create Zoom meeting
    response = client.meeting.create(**meeting_info)

    # Extract meeting link from the response
    meeting_link = response.get('join_url')

    print('meeting link: '+meeting_link)
    # Return meeting link or handle it as needed
    return meeting_link


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
            senior_unicorn_meeting.objects.create(
                user_name=name,
                user_email=email,
                subject=subject,
                message=message,
                meeting_date=date,
                start_time=fromtime,
                end_time=totime
            )
            messages.success(request, "Meeting scheduled with Senior Unicorn.")
            
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
                senior_dragon_meeting.objects.create(
                    user_name=name,
                    user_email=email,
                    subject=subject,
                    message=message,
                    meeting_date=date,
                    start_time=fromtime,
                    end_time=totime
                )
                messages.success(request, "Meeting scheduled with Senior Dragon.")
            else:
                messages.error(request, "No available slots with either Senior Unicorn or Senior Dragon.")  
     
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
    host = request.get_host() # Host 
    paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER, 
            'amount' : price, 
            'item_name' : 'Fast Design Reservation', 
            'invoice' : uuid.uuid4(), 
            'currency' : 'USD', 
            'notify_url' : f'http://{host}{reverse("paypal-ipn")}/',
            'return_url' : f'http://{host}{reverse("call_expert:payment-success")}/',
            'cancel_url' : f'http://{host}{reverse("call_expert:payment-failed")}/',
    }
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
            unicorn_meeting.objects.create(
                user_name=name,
                user_email=email,
                subject=subject,
                message=message,
                meeting_date=date,
                start_time=fromtime,
                end_time=totime,
                upload_file=upload_file
                
            )
            messages.success(request, "Meeting scheduled with Unicorn team.")
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
                dragon_meeting.objects(
                    user_name=name,
                    user_email=email,
                    subject=subject,
                    message=message,
                    meeting_date=date,
                    start_time=fromtime,
                    end_time=totime,
                    upload_file=upload_file
                )
                dragon_meeting.save(commit=False)
                messages.success(request, "Meeting scheduled with Dragon.")
            else:
                messages.error(request, "No available slots with either  Unicorn or Dragon teams.")  
      
        
    paypal = PayPalPaymentsForm(initial=paypal_checkout)
    return render(request, 'callEpertTwo.html', {'paypal' : paypal })



def payment(request):
    pass

def payment_success(request):
    form_data = request.session.get('form_data', None)

    if form_data:
        form_data['is_paid'] = True

        if form_data.get('team') == 'unicorn':
            meeting = unicorn_meeting(**form_data)
        else:
            meeting = dragon_meeting(**form_data)

        meeting.save()

        del request.session['form_data']

        messages.success(request, "Payment successful. Meeting details saved.")
    else:
        messages.error(request, "No form data found.")

    return render(request, 'payment_success.html')


def payment_failed(request):
    pass