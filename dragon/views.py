from django.shortcuts import render
#import httpresponse
from django.http import HttpResponse
from .models import meeting as dragon_meeting , working_setting as dragon_working_setting
from unicorn.models import meeting as unicorn_meeting , working_setting as unicorn_working_setting

from datetime import datetime, timedelta
from django.http import JsonResponse

# Create your views here.
def dragon(request):
    pass


def get_available_time(request):
    #get from request the day_name
    day_name = request.GET.get("dayName")
    date = request.GET.get("date")

    #get available time for dragon team
    available_time_for_dragon = get_available_time_for_dragon_team(day_name, date)
    #get available time for unicorn team
    available_time_for_unicorn = get_available_time_for_unicorn_team(day_name, date)
    
    if not available_time_for_dragon and not available_time_for_unicorn:
        return JsonResponse({'available_times': []})
    
    #avianable time = function to remove deplucate time
    available_time = remove_duplicate_times(available_time_for_dragon, available_time_for_unicorn)
    #return the available time as array of json object
    return JsonResponse({'available_times': available_time})


def remove_duplicate_times(dragon_times, unicorn_times):
    # Combine both lists
    combined_times = dragon_times + unicorn_times

    # Remove duplicates by converting each time slot to a tuple and using a set
    unique_times = set()
    for time_slot in combined_times:
        time_tuple = (time_slot['from'], time_slot['to'])
        unique_times.add(time_tuple)

    # Convert back to the original format
    non_duplicate_times = [{'from': time[0], 'to': time[1]} for time in unique_times]
    
    # Sort the times for better readability and consistency
    non_duplicate_times.sort(key=lambda x: x['from'])

    return non_duplicate_times



def get_available_time_for_dragon_team(day_name, date):
    working_day=dragon_working_setting.objects.filter(day=day_name).first()
    #check if the day is working day
    if working_day is None:
        return []
    
    #get start time and end time from working day
    start_time = working_day.start_time
    end_time = working_day.end_time
    #get meeting duration from working day
    meeting_duration_hour = working_day.meeting_duration_hour
    meeting_duration_minute = working_day.meeting_duration_minute
    #get break time from working day
    break_time_from = working_day.break_time_from
    break_time_to = working_day.break_time_to
    #get meeting price from working day
    meeting_price = working_day.meeting_price
    #fucntion to get the available time
    working_time=calculate_available_time(start_time, end_time, meeting_duration_hour, meeting_duration_minute, break_time_from, break_time_to)
       
    # Assuming 'date' is obtained from the request and formatted as YYYY-MM-DD
    meeting_date = datetime.strptime(date, "%Y-%m-%d").date()

    # Remove reserved times
    available_time = remove_reserved_times_from_dragon_team(working_time, meeting_date)
    
    return available_time
    
def get_available_time_for_unicorn_team(day_name, date):
    working_day=unicorn_working_setting.objects.filter(day=day_name).first()
    #check if the day is working day
    if working_day is None:
        return []
    
    #get start time and end time from working day
    start_time = working_day.start_time
    end_time = working_day.end_time
    #get meeting duration from working day
    meeting_duration_hour = working_day.meeting_duration_hour
    meeting_duration_minute = working_day.meeting_duration_minute
    #get break time from working day
    break_time_from = working_day.break_time_from
    break_time_to = working_day.break_time_to
    #get meeting price from working day
    meeting_price = working_day.meeting_price
    #fucntion to get the available time
    working_time=calculate_available_time(start_time, end_time, meeting_duration_hour, meeting_duration_minute, break_time_from, break_time_to)
       
    # Assuming 'date' is obtained from the request and formatted as YYYY-MM-DD
    meeting_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Remove reserved times
    available_time = remove_reserved_times_from_unicorn_team(working_time, meeting_date)
    
    return available_time
    

def calculate_available_time(start_time, end_time, meeting_duration_hour, meeting_duration_minute, break_time_from, break_time_to):
    available_times = []
    current_time = start_time
    duration = timedelta(hours=meeting_duration_hour, minutes=meeting_duration_minute)

    while current_time < end_time:
        next_time = (datetime.combine(datetime.today(), current_time) + duration).time()
        
        # Check if the current time slot overlaps with the break time
        if not (break_time_from <= current_time < break_time_to) and not (break_time_from < next_time <= break_time_to):
            available_times.append({
                "from": current_time.strftime("%H:%M"),
                "to": next_time.strftime("%H:%M")
            })

        current_time = next_time

    return available_times


def remove_reserved_times_from_dragon_team(available_times, meeting_date):
    # Fetch all meetings for the given date
    reserved_meetings = dragon_meeting.objects.filter(meeting_date=meeting_date)

    # Convert the meeting times to a set of tuples for easier comparison
    reserved_times = {(m.start_time, m.end_time) for m in reserved_meetings}

    # Filter out the available times that overlap with the reserved times
    filtered_times = []
    for time_slot in available_times:
        
        start_time = datetime.strptime(time_slot['from'], "%H:%M").time()
        end_time = datetime.strptime(time_slot['to'], "%H:%M").time()

        overlap = False
        for reserved_start, reserved_end in reserved_times:
            if (start_time < reserved_end and end_time > reserved_start):
                overlap = True
                break
        
        if not overlap:
            filtered_times.append(time_slot)

    return filtered_times


def remove_reserved_times_from_unicorn_team(available_times, meeting_date):
    # Fetch all meetings for the given date
    reserved_meetings = unicorn_meeting.objects.filter(meeting_date=meeting_date)

    # Convert the meeting times to a set of tuples for easier comparison
    reserved_times = {(m.start_time, m.end_time) for m in reserved_meetings}
    print('reserved_times', reserved_times)    
    # Filter out the available times that overlap with the reserved times

    filtered_times = []
    for time_slot in available_times:
        
        start_time = datetime.strptime(time_slot['from'], "%H:%M").time()
        end_time = datetime.strptime(time_slot['to'], "%H:%M").time()

        overlap = False
        for reserved_start, reserved_end in reserved_times:
            if (start_time < reserved_end and end_time > reserved_start):
                overlap = True
                break
        
        if not overlap:
            filtered_times.append(time_slot)

    print('filtered_times', filtered_times)
    return filtered_times
