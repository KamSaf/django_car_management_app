from django.shortcuts import render, redirect
from workshops.forms import WorkshopForm
from workshops.models import Workshop
from cars.models import Car
from cars.forms import CarForm
from entries.forms import EntryForm
from entries.models import Entry
from .utils import get_viewed_car


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

    workshops = Workshop.objects.filter(user=request.user).order_by('create_date').all()
    favourite_workshops = Workshop.objects.filter(user=request.user, favourite=True).order_by('-last_edit_date').all()
    cars = Car.objects.filter(user=request.user).order_by('create_date').all()

    viewed_car = get_viewed_car(user=request.user, car_id=car_id)
    entries = Entry.objects.filter(user=request.user, car=viewed_car).order_by('-date').all()

    last_entry = Entry.objects.filter(car=viewed_car).order_by('-date').first()
    viewed_car_mileage = last_entry.mileage if last_entry else 0

    # create forms
    new_workshop_form = WorkshopForm(logged_user=request.user)
    new_car_form = CarForm(logged_user=request.user)
    new_entry_form = EntryForm(logged_user=request.user, car=viewed_car)
    edit_car_form = CarForm(instance=viewed_car, logged_user=request.user)
    edit_car_form.set_initial(car=viewed_car)

    return render(
        request=request,
        template_name='home.html',
        context={
            'new_workshop_form': new_workshop_form,
            'new_car_form': new_car_form,
            'new_entry_form': new_entry_form,
            'edit_car_form': edit_car_form,
            'cars': cars,
            'viewed_car': viewed_car,
            'viewed_car_mileage': viewed_car_mileage,
            'workshops': workshops,
            'favourite_workshops': favourite_workshops,
            'entries': entries,
        }
    )
