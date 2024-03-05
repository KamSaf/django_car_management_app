from django.shortcuts import render, redirect
from .forms import CarForm
from .models import Car
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


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
