import os
import django
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

# Konfiguracja środowiska Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dummy_settings_for_script")
import django.conf

# Konfiguracja bazy danych ręcznie przez URI
DATABASE_URL = "postgresql://django_app:24isH2G7eb3LlJF4TLZhgohgj7a3sLS0@dpg-d186ee6mcj7s73b53oh0-a.frankfurt-postgres.render.com/db_django_ijvt"

django.conf.settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "db_django_ijvt",
            "USER": "django_app",
            "PASSWORD": "24isH2G7eb3LlJF4TLZhgohgj7a3sLS0",
            "HOST": "dpg-d186ee6mcj7s73b53oh0-a.frankfurt-postgres.render.com",
            "PORT": "5432",
        }
    },
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "cronjob",
    ],
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

# Import modelu po skonfigurowaniu Django
from cronjob.models import (
    FuelPrices,
)  # Zamień 'your_app_name' na nazwę swojej aplikacji


def get_fuel_prices():
    """
    Scrapes fuel prices from AutoCentrum
    Returns: [pb95, pb98, diesel, diesel_premium, lpg]
    """
    URL = "https://www.autocentrum.pl/paliwa/ceny-paliw/"
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")
    return [
        float(item.text.strip()[0:4].replace(",", "."))
        for item in soup.find_all(class_="price")
    ]


def save_prices(prices):
    """
    Saves scraped prices to database
    """
    prices = [price if isinstance(price, float) else None for price in prices]
    FuelPrices.objects.create(
        pb95=prices[0],
        pb98=prices[1],
        diesel=prices[2],
        diesel_premium=prices[3],
        lpg=prices[4],
        date=timezone.now(),
    ).save()


if __name__ == "__main__":
    fuel_prices = get_fuel_prices()
    save_prices(fuel_prices)
    print("Fuel prices updated!")
