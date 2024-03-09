from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import EntryForm
from .models import Entry
from django.shortcuts import render
from django.utils import timezone
from car_management_app.utils import get_viewed_car
from cars.models import Car


@api_view(['POST'])
@login_required
def async_add_entry(request):
    """
        Endpoint for creating new exploitation histroy entry (for AJAX)
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

        form = EntryForm(request.POST, logged_user=request.user, car=car)
        form.clear_errors()
        if form.is_valid():
            form.save()
            return Response({'status': 'success'})
    return Response({
        'status': 'fail',
        'errors': form.data_errors,
    })
