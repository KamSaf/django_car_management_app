from django.shortcuts import render, redirect
from workshops.forms import WorkshopForm
from workshops.models import Workshop
from cars.models import Car
from cars.forms import CarForm
from entries.forms import EntryForm
from entries.models import Entry
from reminders.models import Reminder
from reminders.forms import ReminderForm
from .utils import get_viewed_car, expl_report
from django.utils import timezone


def welcome(request):
    """
        View rendering welcome page
    """
    return render(request=request, template_name='welcome.html')


def about(request):
    """
        View rendering about page with app and author contact info
    """
    return render(request=request, template_name='about.html')


def refresh_navbar(request):
    """
        Endpoint returnig navbar template (for AJAX navbar refresh)
    """
    return render(
        request=request,
        template_name='include/navbar.html',
        context={'user': request.user}
    )


def home(request, car_id=None):
    """
        View for rendering home page.
        If car_id is defined then this car is being displayed, else favourite car or first car (if there is no favourite) in database is displayed.
    """
    if not request.user.is_authenticated:
        return redirect(to='welcome_page')

    cars = Car.objects.filter(user=request.user).order_by('create_date').all()
    if len(cars) == 0:
        return redirect(to='add_new_car', first='true')

    workshops = Workshop.objects.filter(user=request.user).order_by('create_date').all()
    favourite_workshops = workshops.filter(favourite=True).order_by('id', '-last_edit_date')

    viewed_car = get_viewed_car(user=request.user, car_id=car_id)
    entries = Entry.objects.filter(user=request.user, car=viewed_car).order_by('-date', '-create_date').all()

    last_entry = Entry.objects.filter(car=viewed_car).order_by('-date').first()
    viewed_car_mileage = last_entry.mileage if last_entry else 0

    reminders = Reminder.objects.filter(car=viewed_car, date__gte=timezone.now()).order_by('date').all()
    this_month_report, last_month_report = expl_report(car=viewed_car, year=timezone.now().year, month=timezone.now().month)

    return render(
        request=request,
        template_name='home.html',
        context={
            'new_workshop_form': WorkshopForm(logged_user=request.user),
            'new_car_form': CarForm(logged_user=request.user),
            'new_entry_form': EntryForm(logged_user=request.user, car=viewed_car),
            'new_reminder_form': ReminderForm(logged_user=request.user, car=viewed_car),
            'edit_car_form': CarForm(instance=viewed_car, logged_user=request.user).set_initial(car=viewed_car),
            'cars': cars,
            'viewed_car': viewed_car,
            'viewed_car_mileage': viewed_car_mileage,
            'workshops': workshops,
            'favourite_workshops': favourite_workshops,
            'entries': entries,
            'reminders': reminders,
            'this_month_data': this_month_report,
            'last_month_data': last_month_report,
        }
    )
