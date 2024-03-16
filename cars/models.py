from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.TextField(blank=False, max_length=100)
    model = models.TextField(blank=False, max_length=100)
    prod_year = models.TextField(blank=True, max_length=100)
    num_plate = models.TextField(blank=False, max_length=50)
    fuel_type = models.TextField(blank=True, max_length=50)
    displacement = models.IntegerField(blank=True)
    vin = models.TextField(blank=True, max_length=25)
    favourite = models.BooleanField(default=False, blank=False)
    create_date = models.DateTimeField(default=timezone.now)
    last_edit_date = models.DateTimeField(default=timezone.now)

    def get_display_fields(self) -> dict:
        """
            Returns dict containing Car object data
        """
        from entries.models import Entry

        last_entry = Entry.objects.filter(car=self).order_by('-date').first()
        mileage = last_entry.mileage if last_entry else 0

        return [
            (self.make, 'Make', 'car-front', None),
            (self.model, 'Model', 'box', None),
            (self.prod_year, 'Production year', 'calendar', None),
            (self.num_plate, 'Number plate', '123', None),
            (self.fuel_type, 'Fuel type', 'fuel-pump', None),
            (self.displacement, 'Displacement', 'arrows-angle-expand', 'cm3'),
            (mileage, 'Mileage', 'arrows-angle-expand', 'km'),
            (self.vin, 'VIN number', 'pencil-square', None)
        ]