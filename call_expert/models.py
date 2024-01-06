from django.db import models
from django.contrib.auth.models import User

# Create your models here.
type={
    ('normal','normal'),
    ('professional','professional'),
}
class call_expert(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    call_type=models.CharField(max_length=20,choices=type,default='normal')
    date=models.DateTimeField()
    
    def __str__(self):
        return self.user.username
    
    #order depend on date
    class Meta:
        ordering=['date']
        
        
#upload file for the meeting
class upload_file(models.Model):
    file=models.FileField(upload_to='files/')
    
    def __str__(self):
        #return id
        return str(self.id)
    
        

    