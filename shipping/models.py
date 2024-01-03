from django.db import models

# Create your models here.
class Shipping_price(models.Model):
    price = models.IntegerField()
    def __str__(self):
        return str(self.price)
    
