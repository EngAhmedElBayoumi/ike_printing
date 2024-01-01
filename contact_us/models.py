from django.db import models

# Create your models here.

#contact us model
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return self.name
    
    
    

#contact list model (first_name , last_name , email ,address, phone_number , gender , birth_date ,language , notes)
class ContactList(models.Model):
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,blank=True)
    birth_date=models.CharField(max_length=100,null=True,blank=True)
    language=models.CharField(max_length=100,null=True,blank=True)
    notes=models.TextField(max_length=1000,null=True,blank=True)
    
    def __str__(self):
        return self.email
    

    
    