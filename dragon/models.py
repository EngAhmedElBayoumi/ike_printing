from django.db import models
from datetime import datetime, timedelta



# Create your models here.


#days all the days of the week
days = (
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
    ('Sunday','Sunday'),
)

class working_setting(models.Model):
    day = models.CharField(max_length=10,choices=days)
    start_time = models.TimeField()
    end_time = models.TimeField()
    #meeting time duration by hour and minute
    meeting_duration_hour = models.IntegerField(null=True,blank=True)
    meeting_duration_minute = models.IntegerField(null=True,blank=True)
    #break time duration by hour and minute
    break_time_from = models.TimeField()
    break_time_to = models.TimeField()
    meeting_price = models.FloatField()

    def __str__(self):
        return self.day
 
class upload_file(models.Model):
    file = models.FileField(upload_to='uploads/meetings',null=True,blank=True)
    def __str__(self):
        #id
        return str(self.id)   

#reserving meeting data and time
class meeting(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(null=True,blank=True)
    meeting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    #meeting files
    files = models.ManyToManyField(upload_file,null=True,blank=True)
    meeting_url=models.CharField(max_length=5000,null=True,blank=True)

    def __str__(self):
        return str(self.meeting_date)
    
    

