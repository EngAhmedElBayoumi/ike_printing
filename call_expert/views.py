from django.shortcuts import render
from dragon.models import working_setting as dragon_working_setting , meeting as dragon_meeting 
from senior_dragon.models import working_setting as senior_dragon_working_setting , meeting as senior_dragon_meeting
from unicorn.models import working_setting as unicorn_working_setting , meeting as unicorn_meeting
from senior_unicorn.models import working_setting as senior_unicorn_working_setting , meeting as senior_unicorn_meeting
from datetime import datetime
#import messages
from django.contrib import messages
# Create your views here.

def call_expert(request):
    return render(request, 'ChooseDesigner.html', {})

#CallSeniorDesigner
def call_senior_designer(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        fromtime=request.POST.get('fromtime')
        totime=request.POST.get('totime')
        date=request.POST.get('data')
        print(date)
        #convert fromtime from string to time not datetime
        fromtime = datetime.strptime(fromtime, '%H:%M').time()
        #convert totime from string to time not datetime
        totime = datetime.strptime(totime, '%H:%M').time()
        date = datetime.strptime(date, '%Y-%m-%d').date()
        print(date)

        
        #set meeting to senior dragon or senior unicorn if the time is available in senior unicorn or senior dragon
        #get all senior dragon meetings 
        unicorn_conflict = senior_unicorn_meeting.objects.filter(meeting_date=date, start_time__lte=totime, end_time__gte=fromtime).exists()
        #get break time from working day to unicorn team
        break_time_from = senior_unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
        break_time_to = senior_unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
        #check if time is in break time
        if fromtime >= break_time_from and totime <= break_time_to:
            #conflict true
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

#call designer
def call_designer(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        fromtime=request.POST.get('fromtime')
        totime=request.POST.get('totime')
        date=request.POST.get('data')
        print(date)
        #convert fromtime from string to time not datetime
        fromtime = datetime.strptime(fromtime, '%H:%M').time()
        #convert totime from string to time not datetime
        totime = datetime.strptime(totime, '%H:%M').time()
        date = datetime.strptime(date, '%Y-%m-%d').date()
        print(date)

        
        #set meeting to senior dragon or senior unicorn if the time is available in senior unicorn or senior dragon
        #get all senior dragon meetings 
        unicorn_conflict = unicorn_meeting.objects.filter(meeting_date=date, start_time__lt=totime, end_time__gt=fromtime).exists()        
        
        #get break time from working day to unicorn team
        break_time_from = unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_from
        break_time_to = unicorn_working_setting.objects.filter(day=date.strftime("%A")).first().break_time_to
        #check if time is in break time
        if fromtime >= break_time_from and totime <= break_time_to:
            #conflict true
            unicorn_conflict = True
        
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
                end_time=totime
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
                dragon_meeting.objects.create(
                    user_name=name,
                    user_email=email,
                    subject=subject,
                    message=message,
                    meeting_date=date,
                    start_time=fromtime,
                    end_time=totime
                )
                messages.success(request, "Meeting scheduled with Dragon.")
            else:
                messages.error(request, "No available slots with either  Unicorn or Dragon teams.")  
      
        
    return render(request, 'callEpertTwo.html', {})

