from django.db import models
from django.utils import timezone


class FuelPrices(models.Model):
    pb95 = models.FloatField(null=True)
    pb98 = models.FloatField(null=True)
    diesel = models.FloatField(null=True)
    diesel_premium = models.FloatField(null=True)
    lpg = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def get_data(self) -> dict:
        """
            Returns dict containing object data
        """
        return {
            'PB95': self.pb95,
            'PB98': self.pb98,
            'Diesel': self.diesel,
            'Diesel+': self.diesel_premium,
            'LPG': self.lpg,
            'Date': self.date.strftime("%a %d %b %Y")
        }
