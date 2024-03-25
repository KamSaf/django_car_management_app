from cars.models import Car
from django.contrib.auth.models import User
from entries.models import Entry
import calendar
from django.utils import timezone


def get_viewed_car(user: User, car_id: int = None) -> Car | None:
    """
        Get Car object to display on the home page
    """
    viewed_car = None
    cars = Car.objects.filter(user=user).all()
    if car_id:
        viewed_car = cars.filter(id=car_id).first()

    if not viewed_car:
        try:
            viewed_car = cars.get(favourite=True)
        except Car.DoesNotExist:
            viewed_car = cars[0]

    return viewed_car


def costs_sum(query, category: str = None) -> float:
    """
        Calculate sum of costs of given entries
    """
    if category:
        query = query.filter(category=category)
    return sum(query.values_list('cost', flat=True))


def calc_report(car: Car, year: int, month: int) -> dict:
    """
        Calculate exploitation data for given month
    """
    month_days = timezone.now().day if timezone.now().month == month and timezone.now().year == year else calendar.monthrange(year, month)[1]
    entries = Entry.objects.filter(car=car).order_by('date')

    if month > 1:
        last_month = month - 1
        last_year = year
    else:
        last_month = 12
        last_year = year - 1

    previous_month_entries = entries.filter(date__year=last_year, date__month=last_month)
    this_month_entries = entries.filter(date__year=year, date__month=month)

    start_entry = previous_month_entries.last() if previous_month_entries.last() else this_month_entries.first()
    end_entry = this_month_entries.last()

    start_mileage = start_entry.mileage if start_entry else 0
    end_mileage = end_entry.mileage if end_entry else 0

    mileage_covered = end_mileage - start_mileage if end_mileage and start_mileage else 0

    fuel_economy = (sum(this_month_entries.filter(category='fuel').values_list('fuel_liters', flat=True)) * 100) / mileage_covered if mileage_covered else 0
    all_costs = costs_sum(query=this_month_entries)
    fuel_costs = costs_sum(query=this_month_entries, category='fuel')
    service_costs = costs_sum(query=this_month_entries, category='service')
    others_costs = costs_sum(query=this_month_entries, category='others')

    report = {
        'all_costs': all_costs,
        'fuel_costs': round((fuel_costs / all_costs) * 100, 1) if all_costs > 0 else 0,
        'service_costs': round((service_costs / all_costs) * 100, 1) if all_costs > 0 else 0,
        'others_costs': round((others_costs / all_costs) * 100, 1) if all_costs > 0 else 0,
        'cost_per_day': round((all_costs / month_days), 2),
        'cost_per_km': round(fuel_costs / mileage_covered, 2) if mileage_covered > 0 else 0,
        'fuel_economy': round(fuel_economy, 2),
    }
    return report


def expl_report(car: Car, year: int, month: int) -> tuple:
    """
        Create exploitation report for this and last months
    """
    this_month_report = calc_report(car=car, year=year, month=month)
    if month > 1:
        month -= 1
    else:
        month, year = 12, year - 1
    last_month_report = calc_report(car=car, year=year, month=month)
    return this_month_report, last_month_report


def permission_denied() -> dict:
    """
        Returns JSON response for permission denied Response
    """
    return {
        'status': 'fail',
        'errors':
        {
            'access_error': 'You are not permitted to perform this action.'
        },
    }


def item_not_existing(item: str) -> dict:
    """
        Returns JSON response for item does not exists Response
    """
    return {
        'status': 'fail',
        'errors': f'This {item} does not exist.',
    }