from django.contrib import admin
from .models import working_setting , meeting ,upload_file
# Register your models here.

#displaying the models in the admin page 
#woking setting display day and start time and end time and meeting_price
class working_setting_display(admin.ModelAdmin):
    list_display = ('day','start_time','end_time','meeting_price')
    
#meeting display user_name and user_email and subject and message and meeting_date and start_time and end_time
class meeting_display(admin.ModelAdmin):
    list_display = ('user_name','user_email','subject','message','meeting_date','start_time','end_time','display_images')
    
    def display_images(self,obj):
        #get all the files for the meeting
        files = obj.files.all()
        #if there is no files return nothing
        if not files:
            return None
        #return the all files for the meeting in image format
        images_html = ''
        for file in files:
            images_html += '<a href={} download><img src="{}" width="100" height="100"/></a>'.format(file.file.url,file.file.url)
        return format_html(images_html)
admin.site.register(working_setting,working_setting_display)
admin.site.register(meeting,meeting_display)
admin.site.register(upload_file)