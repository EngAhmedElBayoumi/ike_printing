from django.db import models
#import user
from django.contrib.auth.models import User

# Create your models here.

#state in america for choices
STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'), 
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'), 
    ('DE', 'Delaware'), 
    ('DC', 'District Of Columbia'), 
    ('FL', 'Florida'), 
    ('GA', 'Georgia'), 
    ('HI', 'Hawaii'), 
    ('ID', 'Idaho'), 
    ('IL', 'Illinois'), 
    ('IN', 'Indiana'), 
    ('IA', 'Iowa'), 
    ('KS', 'Kansas'), 
    ('KY', 'Kentucky'), 
    ('LA', 'Louisiana'), 
    ('ME', 'Maine'), 
    ('MD', 'Maryland'), 
    ('MA', 'Massachusetts'), 
    ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), 
    ('MS', 'Mississippi'), 
    ('MO', 'Missouri'), 
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'), 
    ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), 
    ('NM', 'New Mexico'), 
    ('NY', 'New York'), 
    ('NC', 'North Carolina'), 
    ('ND', 'North Dakota'), 
    ('OH', 'Ohio'), 
    ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), 
    ('PA', 'Pennsylvania'), 
    ('RI', 'Rhode Island'), 
    ('SC', 'South Carolina'), 
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'), 
    ('TX', 'Texas'), 
    ('UT', 'Utah'), 
    ('VT', 'Vermont'), 
    ('VA', 'Virginia'), 
    ('WA', 'Washington'), 
    ('WV', 'West Virginia'), 
    ('WI', 'Wisconsin'), 
    ('WY', 'Wyoming'),
)

#country choices america 
COUNTRY_CHOICES = (
    ('US', 'United States'),
)



#profile user , image , phone , address , city , state , country , postal_code
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="users/profile_image",blank=True , null=True)
    phone=models.CharField(max_length=20,blank=True)
    address=models.CharField(max_length=200,blank=True)
    address_line2=models.CharField(max_length=200,blank=True,null=True)
    state=models.CharField(max_length=2,choices=STATE_CHOICES,blank=True)
    city=models.CharField(max_length=100,blank=True)
    postal_code=models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return self.user.username
    


    


