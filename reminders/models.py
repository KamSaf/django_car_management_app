from django.db import models
from django.contrib.auth.models import User
from cars.models import Car
from django.utils import timezone
from entries.models import Entry


class Reminder(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    category = models.TextField(blank=False, choices=Entry.TYPES_OF_ENTRIES)
    date = models.DateTimeField(blank=False)
    place = models.TextField(blank=True, max_length=200)
    details = models.TextField(blank=True, max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    last_edit_date = models.DateTimeField(default=timezone.now)

    def get_display_fields(self) -> dict:
        """
            Returns dict containing object data ready to display
        """

        return [
            (self.date.strftime("%a %d %b %Y"), 'Date', '', None),
            (self.category, 'Category', '', None),
            (self.place, 'Place', '', None),
            (self.details, 'Details', '', None),
        ]
