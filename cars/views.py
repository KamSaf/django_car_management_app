from django.shortcuts import render, redirect
from .forms import CarForm
from .models import Car
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view


@login_required
def add_new_car(request):
    """
        View for adding new car to the database
    """
    if not request.user.is_authenticated:
        messages.error(request, 'You have no permission do perform this action.')

    if request.method == 'POST':
        form = CarForm(request.POST, logged_user=request.user)
        form.clear_errors()
        if form.is_valid():
            form.save()
            messages.success(request, 'New car added!')
            return redirect(to="home_page")
        errors = ''
        for value in form.data_errors.values():
            errors = errors.join(value)
        messages.error(request, errors)
        return redirect(to="home_page")


@api_view(['POST'])
@login_required
def async_toggle_favourite_car(request):
    """
        Endpoint for toggling favourite car (for AJAX)
    """
    car_id = request.POST.get('car_id')

    current_favourite_car = Car.objects.filter(favourite=True).first()

    if current_favourite_car:
        current_favourite_car.favourite = False
        current_favourite_car.save()

        if current_favourite_car.id == car_id:
            return Response({'status': 'success'})

    try:
        new_favourite_car = Car.objects.get(id=car_id)
        new_favourite_car.favourite = True
        new_favourite_car.save()
        return Response({'status': 'success'})

    except Car.DoesNotExist:
        return Response({'status': 'failed', 'error': 'This car does not exist.'})
