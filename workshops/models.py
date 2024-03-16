from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Workshop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=False, max_length=100)
    city = models.TextField(blank=False, max_length=100)
    address = models.TextField(blank=False, max_length=100)
    phone_number = models.TextField(blank=False, max_length=9)
    profession = models.TextField(blank=False, max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    favourite = models.BooleanField(default=False, blank=False)
    last_edit_date = models.DateTimeField(default=timezone.now)

    def get_display_fields(self) -> dict:
        """
            Returns dict containing object data
        """
        phone_number = ''.join(['tel. ', self.phone_number[0:3], ' ', self.phone_number[3:6], ' ', self.phone_number[6:9]])
        return [
            (self.name, 'Name', 'person-vcard', None),
            (self.city, 'City', 'map', None),
            (self.address, 'Address', 'geo-alt', None),
            (phone_number, 'Phone number', 'telephone', None),
            (self.profession, 'Profession', 'wrench-adjustable-circle', None),
        ]
