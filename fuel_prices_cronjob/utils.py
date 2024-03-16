from django.utils import timezone
from fuel_prices_cronjob.models import FuelPrices
import requests
from bs4 import BeautifulSoup


def get_fuel_prices() -> list:
    """
        Function scrapping data about current prices (in Poland) from Autocentrum

        Returns prices in order:
        [pb95, pb98, diesel, diesel_premium, lpg]
    """
    URL = 'https://www.autocentrum.pl/paliwa/ceny-paliw/'
    soup = BeautifulSoup(requests.get(URL), 'html.parser')
    return [item.text.strip()[0:4] for item in soup.find_all(class_='price')]


def save_prices(prices: list) -> None:
    """
        Save current fuel prices to the database

        Parameters:
        list of prices in order:
        [pb95, pb98, diesel, diesel_premium, lpg]
    """
    prices = [price if isinstance(price, float) else None for price in prices]
    FuelPrices.objects.new(pb95=prices[0], pb98=prices[1], diesel=prices[2], diesel_premium=prices[3], lpg=prices[4], date=timezone.now()).save()
