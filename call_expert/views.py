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
from .models import upload_file  as UploadFiles

#import messages
from django.contrib import messages
#import zoom
from zoomus import ZoomClient
#import settings
from django.conf import settings
#import redirect
from django.shortcuts import redirect
#import json
import json
import requests
import json
#import datetime
from datetime import datetime, timedelta
#send mail
from django.core.mail import send_mail

# Create your views here.



import os


#create zoom meeting    
def create_zoom_meeting(start_time, duration, topic):
    # Create a Zoom client
    client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET, settings.ZOOM_ACCOUNT_ID)

    # Check if start_time is a string and convert it to a datetime object
        
    # Create a Zoom meeting
    meeting_info = client.meeting.create(user_id='me',
                                         topic=topic,
                                         type=2,  
                                         start_time=datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ'),
                                         duration=duration,
                                         timezone='UTC',
                                         settings={
                                            "host_video": True,
                                            "participant_video": True,
                                            "cn_meeting": False,
                                            "in_meeting": False,
                                            "join_before_host": False,
                                            "mute_upon_entry": False,
                                            "watermark": False,
                                            "use_pmi": False,
                                            "approval_type": 0,
                                            "registration_type": 2,
                                            "audio": "both",
                                            "auto_recording": "none",
                                            "enforce_login": False,
                                            "enforce_login_domains": "",
                                            "alternative_hosts": "",
                                            "close_registration": False,
                                            "registrants_confirmation_email": True,
                                            "waiting_room": True,
                                            "global_dial_in_countries": [],
                                            "global_dial_in_numbers": [],
                                            "contact_name": "",
                                            "contact_email": "",
                                            "registrants_email_notification": True,
                                            "meeting_authentication": False
                                        }
                                        
                                        
                                         )
        


    #meeting url
    meeting_info = meeting_info.json()
    print('meeting_info', meeting_info)
    meeting_url=meeting_info.get('join_url')
    return meeting_url



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
        upload_file=request.FILES.getlist('upload_file') or None
        
        
        
        
        #validate all fields
        if not name or not email or not subject or not message or not fromtime or not totime or not date:
            messages.error(request, "All fields are required.")
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
                'price': price,
            }
            #save upload file to database and get id of files and save it to session
            files_id = []
            if upload_file:
                for file in upload_file:
                    file = UploadFiles.objects.create(file=file)
                    files_id.append(file.id)
            
            request.session['meeting_data']['files_id'] = files_id
                         
            
            
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
                    'price': price,
                }
                files_id = []
                if upload_file:
                    for file in upload_file:
                        file = UploadFiles.objects.create(file=file)
                        files_id.append(file.id)
                
                request.session['meeting_data']['files_id'] = files_id
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
        upload_file=request.FILES.getlist('upload_file') or None
        
        
        #validate all fields
        if not name or not email or not subject or not message or not fromtime or not totime or not date :
            messages.error(request, "All fields are required.")
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
    
        #check if the time is not exist in senior unicorn meetings add meeting to senior unicorn else check in senior dragon meetings 
        if not unicorn_conflict:
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
                'price': price,
            }
            files_id = []
            if upload_file:
                for file in upload_file:
                    file = UploadFiles.objects.create(file=file)
                    files_id.append(file.id)
            request.session['meeting_data']['files_id'] = files_id
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
                    'price': price,
                }
                files_id = []
                if upload_file:
                    for file in upload_file:
                        file = UploadFiles.objects.create(file=file)
                        files_id.append(file.id)
                request.session['meeting_data']['files_id'] = files_id
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
            'return_url' : f'http://{host}{reverse("call_expert:payment_success")}',
            'cancel_url' : f'http://{host}{reverse("call_expert:payment_failed")}',
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
        #calculate deuration
        start_time = meeting_data['start_time']
        end_time = meeting_data['end_time']
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        duration = end_time - start_time
        duration = duration.seconds / 60
        meeting_datetime = datetime.strptime(meeting_data['meeting_date'] + ' ' + meeting_data['start_time'], '%Y-%m-%d %H:%M')
        #create zoom meeting
        meeting_url = create_zoom_meeting(meeting_data['meeting_date'] + 'T' + meeting_data['start_time'] + ":00"+ 'Z', duration, meeting_data['subject'])
        #save meeting
        dragon_meeting_instance=dragon_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
            meeting_url=meeting_url,
        )
        #get all files id
        files_id = meeting_data['files_id']
        if files_id:
            #get all files from database
            files = UploadFiles.objects.filter(id__in=files_id)
            #save files to meeting
            dragon_meeting_instance.files.set(files)
          
        #send mail to user
        send_mail(
            'Fast Meeting Reservation',
            'Your meeting is scheduled successfully and the meeting url is: ' + meeting_url,
            settings.EMAIL_HOST_USER,
            [meeting_data['user_email']],
            fail_silently=False,
        )   
    elif meeting_type == 'unicorn':
        #calculate deuration
        start_time = meeting_data['start_time']
        end_time = meeting_data['end_time']
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        duration = end_time - start_time
        duration = duration.seconds / 60
        #create zoom meeting
        meeting_datetime = datetime.strptime(meeting_data['meeting_date'] + ' ' + meeting_data['start_time'], '%Y-%m-%d %H:%M')
        meeting_url = create_zoom_meeting(meeting_data['meeting_date'] + 'T' + meeting_data['start_time'] + ":00"+ 'Z', duration, meeting_data['subject'])
        
        unicorn_meeting_instance=unicorn_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
            meeting_url=meeting_url
        )
        #get all files id
        files_id = meeting_data['files_id']
        if files_id:
            #get all files from database
            files = UploadFiles.objects.filter(id__in=files_id)
            #save files to meeting
            unicorn_meeting_instance.files.set(files)
        
        
        #send mail to user
        send_mail(
            'Fast Meeting Reservation',
            'Your meeting is scheduled successfully and the meeting url is: ' + meeting_url,
            settings.EMAIL_HOST_USER,
            [meeting_data['user_email']],
            fail_silently=False,
        )
        
    elif meeting_type == 'senior_dragon':
        #calculate deuration
        start_time = meeting_data['start_time']
        end_time = meeting_data['end_time']
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        duration = end_time - start_time
        duration = duration.seconds / 60
        #create zoom meeting
        meeting_datetime = datetime.strptime(meeting_data['meeting_date'] + ' ' + meeting_data['start_time'], '%Y-%m-%d %H:%M')
        meeting_url = create_zoom_meeting(meeting_data['meeting_date'] + 'T' + meeting_data['start_time'] + ":00"+ 'Z', duration, meeting_data['subject'])
        senior_dragon_meeting_instance=senior_dragon_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
            meeting_url=meeting_url
        )
        #get all files id
        files_id = meeting_data['files_id']
        if files_id:
            #get all files from database
            files = UploadFiles.objects.filter(id__in=files_id)
            #save files to meeting
            senior_dragon_meeting_instance.files.set(files)
        
        #send mail to user
        send_mail(
            'profissional Meeting Reservation',
            'Your meeting is scheduled successfully and the meeting url is: ' + meeting_url,
            settings.EMAIL_HOST_USER,
            [meeting_data['user_email']],
            fail_silently=False,
        )
        
        
    elif meeting_type == 'senior_unicorn':
        #calculate deuration
        start_time = meeting_data['start_time']
        end_time = meeting_data['end_time']
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        duration = end_time - start_time
        duration = duration.seconds / 60
        #create zoom meeting
        meeting_datetime = datetime.strptime(meeting_data['meeting_date'] + ' ' + meeting_data['start_time'], '%Y-%m-%d %H:%M')
        meeting_url = create_zoom_meeting(meeting_data['meeting_date'] + 'T' + meeting_data['start_time'] + ":00"+ 'Z', duration, meeting_data['subject'])
        senior_unicorn_meeting_instance = senior_unicorn_meeting.objects.create(
            user_name=meeting_data['user_name'],
            user_email=meeting_data['user_email'],
            subject=meeting_data['subject'],
            message=meeting_data['message'],
            meeting_date=meeting_data['meeting_date'],
            start_time=meeting_data['start_time'],
            end_time=meeting_data['end_time'],
            meeting_url=meeting_url
        )

        # get all files id
        files_id = meeting_data['files_id']
        if files_id:
            # get all files from database
            files = UploadFiles.objects.filter(id__in=files_id)

            # save files to meeting
            senior_unicorn_meeting_instance.files.set(files)
        
        #send mail to user
        send_mail(
            'profissional Meeting Reservation',
            'Your meeting is scheduled successfully and the meeting url is: ' + meeting_url,
            settings.EMAIL_HOST_USER,
            [meeting_data['user_email']],
            fail_silently=False,
        )
        
        
    #clear session
    request.session['meeting_type'] = None
    request.session['meeting_data'] = None
    request.session['files_id'] = None
    messages.success(request, "Your payment is done successfully and your meeting is scheduled.")
    return redirect('call_expert:call_expert')



def payment_failed(request):
    #clear session
    request.session['meeting_type'] = None
    request.session['meeting_data'] = None
    request.session['files_id'] = None
    messages.error(request, "Your payment is failed.")
    return redirect('call_expert:call_expert')