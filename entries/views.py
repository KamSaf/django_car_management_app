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
        Endpoint for creating new exploitation history entry (for AJAX)
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


@api_view(['POST'])
@login_required
def async_edit_entry(request):
    """
        Endpoint for creating new exploitation history entry (for AJAX)
    """
    if request.method == 'POST':
        entry_id = int(request.POST.get('entry_id'))

        try:
            entry = Entry.objects.get(id=entry_id)
        except Entry.DoesNotExist:
            return Response({
                'status': 'fail',
                'errors': 'This entry does not exist in the database.',
            })

        form = EntryForm(request.POST, logged_user=request.user, car=entry.car, instance=entry)
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
def async_load_entries_list(request):
    """
        Endpoint for loading exploitation history entries (for AJAX)
    """

    entries = Entry.objects.filter(user=request.user).order_by('-date', '-create_date').all()

    return render(
        request=request,
        template_name='include/entries/entries_list.html',
        context={'entries': entries},
    )


@api_view(['GET'])
@login_required
def async_load_entry_details(request, entry_id):
    """
        Endpoint for refreshing displayed entry data (for AJAX)
    """
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Entry not found',
        })

    edit_entry_form = EntryForm(instance=entry, logged_user=request.user, car=entry.car)
    return render(
        request=request,
        template_name='include/entries/entry_details.html',
        context={
            'entry': entry,
            'edit_entry_form': edit_entry_form,
            }
    )


@api_view(['GET'])
@login_required
def async_delete_entry(request, entry_id):
    """
        Endpoint for deleting entry (for AJAX)
    """
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        return Response({
            'status': 'fail',
            'errors': {
                'db_error': 'This item does not exist in the database.'
            },
        })
    if request.user.id != entry.user_id:
        return Response({
            'status': 'fail',
            'errors': {
                'access_error': 'You are not permitted to perform this action.'
            },
        })

    entry.delete()
    return Response({'status': 'success'})
