from django.shortcuts import redirect, render
from .forms import CarForm
from .models import Car
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from car_management_app.utils import permission_denied, item_not_existing


@login_required
def add_new_car(request, first=None):
    """
        View for adding new car to the database
    """
    if not request.user.is_authenticated:
        messages.error(request, 'You have no permission do perform this action.')
        return redirect(to="home_page")

    if request.method == 'GET':
        form = CarForm(logged_user=request.user)
        return render(request=request, template_name='cars/add_first_car.html', context={'form': form})

    if request.method == 'POST':
        form = CarForm(request.POST, logged_user=request.user)
        form.clear_errors()
        if form.is_valid():
            form.save()
            messages.success(request, 'New car added!')
            errors = False
        else:
            errors = ''
            for value in form.data_errors.values():
                errors = errors.join(value)
            messages.error(request, errors)

    if first == 'true' and errors:
        return render(request=request, template_name='cars/add_first_car.html')

    return redirect(to="home_page", car_id=form.instance.id)


@api_view(['POST'])
@login_required
def async_toggle_favourite_car(request):
    """
        Endpoint for toggling favourite car (for AJAX)
    """
    car_id = int(request.POST.get('car_id'))
    current_favourite_car = Car.objects.filter(user=request.user, favourite=True).first()

    try:
        new_favourite_car = Car.objects.get(id=car_id)
        if request.user.id != new_favourite_car.user.id:
            return Response(permission_denied())
    except Car.DoesNotExist:
        return Response(item_not_existing(item='car'))

    if current_favourite_car:
        current_favourite_car.favourite = False
        current_favourite_car.last_edit_date = timezone.now()
        current_favourite_car.save()

        if current_favourite_car.id == car_id:
            return Response({'status': 'success'})

    new_favourite_car.favourite = True
    new_favourite_car.last_edit_date = timezone.now()
    new_favourite_car.save()
    return Response({'status': 'success'})


@login_required
def edit_car(request):
    """
        View for editing car data
    """
    errors = False
    car_id = int(request.POST.get('car_id'))

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        messages.error(request, 'This car does not exist in the database.')
        errors = True

    if not request.user.is_authenticated or request.user.id != car.user.id:
        messages.error(request, 'You have no permission do perform this action.')
        errors = True

    if not errors and request.method == 'POST':
        form = CarForm(request.POST, instance=car, logged_user=request.user)
        form.clear_errors()
        if form.is_valid():
            form.save()
            messages.success(request, 'Data edited!')
        else:
            errors_messages = ''
            for value in form.data_errors.values():
                errors_messages = errors_messages.join(value)
            messages.error(request, errors_messages)
    return redirect(to="home_page")


@login_required
def delete_car(request):
    """
        View for deleting car from database
    """
    errors = False
    car_id = int(request.POST.get('car_id'))

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        messages.error(request=request, message='This car does not exist in the database.')
        errors = True

    if not request.user.is_authenticated or request.user.id != car.user.id:
        messages.error(request=request, message='You have no permission do perform this action.')
        errors = True

    if not errors and request.method == 'POST':
        car.delete()
        messages.success(request=request, message=f'{car.make} {car.model} ({car.num_plate}) has been deleted.')
    else:
        messages.error(request=request, message='Error occured while trying to delete this object.')
    return redirect(to="home_page")
