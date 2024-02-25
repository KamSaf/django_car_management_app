from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Workshop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False, max_length=100)
    city = models.TextField(blank=True, max_length=100)
    address = models.TextField(blank=True, max_length=100)
    phone_number = models.TextField(blank=True, max_length=9)
    profession = models.TextField(blank=True, max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    favourite = models.BooleanField(default=False, blank=False)
    last_edit_date = models.DateTimeField(default=timezone.now)
