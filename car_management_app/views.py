from django.shortcuts import render, redirect
from workshops.forms import WorkshopForm
from workshops.models import Workshop
from cars.models import Car
from cars.forms import CarForm


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


def home(request):
    """
        View for rendering home page
    """
    if request.user.is_authenticated:
        workshops = Workshop.objects.filter(user=request.user).order_by('create_date').all()
        favourite_workshops = Workshop.objects.filter(user=request.user, favourite=True).order_by('-last_edit_date').all()
        cars = Car.objects.filter(user=request.user).order_by('create_date').all()
        try:
            viewed_car = Car.objects.filter(favourite=True).first()
        except Car.DoesNotExist:
            viewed_car = cars[0]
        workshop_form = WorkshopForm(logged_user=request.user)
        car_form = CarForm(logged_user=request.user)
        return render(
            request=request,
            template_name='home.html',
            context={
                'new_workshop_form': workshop_form,
                'new_car_form': car_form,
                'cars': cars,
                'viewed_car': viewed_car,
                'workshops': workshops,
                'favourite_workshops': favourite_workshops
            }
        )
    else:
        return redirect(to='welcome_page')
