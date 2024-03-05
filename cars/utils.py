from django.utils import timezone


def populate_production_year_field(lower_bound: int = 1900, upper_bound: int = timezone.now().year):
    choice_list = []

    for i in range(upper_bound - lower_bound):
        choice_list.append((i, upper_bound - i))

    return choice_list
