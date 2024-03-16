import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_management_app.settings")
django.setup()


def update_fuel_prices():
    from cronjob.utils import save_prices, get_fuel_prices
    save_prices(prices=get_fuel_prices())
