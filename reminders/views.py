from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import ReminderForm
from .models import Reminder
from cars.models import Car
from django.shortcuts import render
from django.utils import timezone


@api_view(['POST'])
@login_required
def async_add_reminder(request):
    """
        Endpoint for creating new reminder (for AJAX)
    """
    if request.method == 'POST':
        car_id = int(request.POST.get('car_id'))

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({
                'status': 'fail',
                'errors': 'This car does not exist in the database.',
            })

        form = ReminderForm(request.POST, logged_user=request.user, car=car)
        form.clear_errors()
        if form.is_valid():
            form.save()
            return Response({'status': 'success'})
    return Response({
        'status': 'fail',
        'errors': form.data_errors,
    })


@api_view(['GET'])
@login_required
def async_load_reminders_list(request, car_id):
    """
        Endpoint for loading reminders list (for AJAX)
    """

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return Response({
            'status': 'fail',
            'errors': 'This car does not exist in the database.',
        })

    reminders = Reminder.objects.filter(user=request.user, car=car, date__gte=timezone.now()).order_by('date').all()

    return render(
        request=request,
        template_name='include/reminders/reminders_list.html',
        context={'reminders': reminders},
    )


@api_view(['GET'])
@login_required
def async_load_reminder_details(request, reminder_id):
    """
        Endpoint for loading reminder data (for AJAX)
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
    except Reminder.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Reminder not found',
        })

    return render(
        request=request,
        template_name='include/reminders/reminder_details.html',
        context={
            'reminder': reminder,
        }
    )


@api_view(['GET'])
@login_required
def async_delete_reminder(request, reminder_id):
    """
        Endpoint for deleting reminder (for AJAX)
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
    except Reminder.DoesNotExist:
        return Response({
            'status': 'fail',
            'errors': {
                'db_error': 'This reminder does not exist in the database.'
            },
        })

    if request.user.id != reminder.user_id:
        return Response({
            'status': 'fail',
            'errors': {
                'access_error': 'You are not permitted to perform this action.'
            },
        })

    reminder.delete()
    return Response({'status': 'success'})
