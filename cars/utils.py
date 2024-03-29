from django.utils import timezone


def years_list(lower_bound: int = 1900, upper_bound: int = timezone.now().year):
    choice_list = []

    for i in range(upper_bound - lower_bound):
        choice_list.append((f'{upper_bound - i}', f'{upper_bound - i}'))

    return choice_list
