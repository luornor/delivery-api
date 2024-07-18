# Create your models here.
from django.db import models
import uuid
from datetime import datetime, timedelta


class Delivery(models.Model):
    DELIVERY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('overnight', 'Overnight'),
    ]
    order_id = models.IntegerField()
    delivery_provider = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('on_hold', 'On Hold'),
        ('ready', 'Ready'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='on_hold')
    current_location = models.CharField(max_length=255, null=True, blank=True) 
    estimated_delivery_time = models.DateTimeField(null=True, blank=True) 
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='standard')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_estimated_delivery_time(self):
        if self.delivery_method == 'standard':
            self.estimated_delivery_time = datetime.now() + timedelta(days=5)
        elif self.delivery_method == 'express':
            self.estimated_delivery_time= datetime.now() + timedelta(days=2)
        elif self.delivery_method == 'overnight':
            self.estimated_delivery_time = datetime.now() + timedelta(days=1)
        return None

    def __str__(self):
        return f'{self.id}'
