from django.shortcuts import render
from .models import FuelPrices


def async_refresh_fuel_prices(request):
    """
        Endpoint refreshing fuel prices table (for AJAX)
    """
    prices = FuelPrices.objects.order_by('-date').first()
    return render(
        request=request,
        template_name='include/fuel_prices.html',
        context={'fuel_prices': prices}
    )
