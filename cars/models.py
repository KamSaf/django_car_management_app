from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.TextField(blank=False, max_length=100)
    model = models.TextField(blank=False, max_length=100)
    prod_year = models.TextField(blank=True, max_length=100)
    num_plate = models.TextField(blank=True, max_length=50)
    fuel_type = models.TextField(blank=True, max_length=50)
    displacement = models.FloatField(blank=True)
    vin = models.TextField(blank=True, max_length=25)
    favourite = models.BooleanField(default=False, blank=False)
    create_date = models.DateTimeField(default=timezone.now)
    last_edit_date = models.DateTimeField(default=timezone.now)
