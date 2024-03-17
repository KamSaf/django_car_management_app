from django.db import models
from django.utils import timezone


class FuelPrices(models.Model):
    pb95 = models.FloatField(null=True)
    pb98 = models.FloatField(null=True)
    diesel = models.FloatField(null=True)
    diesel_premium = models.FloatField(null=True)
    lpg = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def get_data(self) -> list:
        """
            Returns dict containing object data
        """
        return [
            ('PB95', self.pb95, "#55a309"),
            ('PB98', self.pb98, "#4f900f"),
            ('Diesel', self.diesel, "#4a4a4a"),
            ('Diesel+', self.diesel_premium, "#353535"),
            ('LPG', self.lpg, "#00aeef"),
        ]
