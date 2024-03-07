from django.db import models
from django.contrib.auth.models import User
from cars.models import Car
from django.utils import timezone


class Entry(models.Model):

    TYPES_OF_ENTRIES = {
        "service": "Service",
        "fuel": "Fuel",
        "others": "Others",
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cost = models.FloatField(default=0)
    category = models.TextField(blank=False, choices=TYPES_OF_ENTRIES)
    date = models.DateTimeField(blank=False)
    notes = models.TextField(blank=True, max_length=255)
    create_date = models.DateTimeField(default=timezone.now)
    last_edit_date = models.DateTimeField(default=timezone.now)
