from django.contrib import admin
from .models import working_setting , meeting
# Register your models here.

#displaying the models in the admin page 
#woking setting display day and start time and end time and meeting_price
class working_setting_display(admin.ModelAdmin):
    list_display = ('day','start_time','end_time','meeting_price')
    
#meeting display user_name and user_email and subject and message and meeting_date and start_time and end_time
class meeting_display(admin.ModelAdmin):
    list_display = ('user_name','user_email','subject','message','meeting_date','start_time','end_time')
    
admin.site.register(working_setting,working_setting_display)
admin.site.register(meeting,meeting_display)