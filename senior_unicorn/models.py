from django.db import models

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
    break_duration_hour = models.IntegerField(null=True,blank=True)
    break_duration_minute = models.IntegerField(null=True,blank=True)
    meeting_price = models.IntegerField()

    def __str__(self):
        return self.day
    

#reserving meeting data and time
class meeting(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    meeting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return str(self.meeting_date)