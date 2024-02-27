from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import WorkshopForm
from .models import Workshop
from django.shortcuts import render
from django.utils import timezone


@api_view(['POST'])
@login_required
def async_add_workshop(request):
    """
        Endpoint for creating new workshop (for AJAX)
    """
    if request.method == 'POST':
        form = WorkshopForm(request.POST, logged_user=request.user)
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
def async_load_workshop_details(request, workshop_id):
    """
        Endpoint for loading workshop details and edit form (for AJAX)
    """
    try:
        workshop = Workshop.objects.get(id=workshop_id)
    except Exception(Workshop.DoesNotExist):
        return Response({
            'status': 'fail',
            'errors': 'This item does not exist.',
        })
    form = WorkshopForm(instance=workshop, logged_user=request.user)
    form.set_initial(workshop=workshop)

    return render(
        request=request,
        template_name='include/workshops/workshop_details.html',
        context={
            'workshop': workshop,
            'edit_workshop_form': form
        },
    )


@api_view(['POST'])
@login_required
def async_edit_workshop(request, workshop_id):
    """
        Endpoint for editing workshop (for AJAX)
    """
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=workshop_id)
        except Workshop.DoesNotExist:
            return Response({
                'status': 'fail',
                'errors': {
                    'db_error': 'This item does not exist in the database.'
                },
            })
        if request.user.id != workshop.user_id:
            return Response({
                'status': 'fail',
                'errors': {
                    'access_error': 'You are not permitted to perform this action.'
                },
            })
        form = WorkshopForm(request.POST, instance=workshop, logged_user=request.user)
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
def async_toggle_favourite_workshop(request, workshop_id):
    """
        Endpoint for toggling favourite workshop option (for AJAX)
    """
    if request.method == 'POST':
        try:
            workshop = Workshop.objects.get(id=workshop_id)
        except Workshop.DoesNotExist:
            return Response({
                'status': 'fail',
                'errors': {
                    'db_error': 'This item does not exist in the database.'
                },
            })
        if request.user.id != workshop.user_id:
            return Response({
                'status': 'fail',
                'errors': {
                    'access_error': 'You are not permitted to perform this action.'
                },
            })
        if workshop:
            workshop.last_edit_date = timezone.now()
            workshop.favourite = not workshop.favourite
            workshop.save()
        if workshop and workshop.favourite:
            return Response({'status': 'success', 'state': 'toggled'})
        else:
            return Response({'status': 'success', 'state': 'untoggled'})


@api_view(['GET'])
@login_required
def async_load_favourite_workshops_list(request):
    """
        Endpoint for loading favourite workshops list (for AJAX)
    """
    favourite_workshops = Workshop.objects.filter(user=request.user, favourite=True).order_by('-last_edit_date').all()

    return render(
        request=request,
        template_name='include/workshops/favourite_workshops_list.html',
        context={'favourite_workshops': favourite_workshops}
    )


@api_view(['GET'])
@login_required
def async_load_workshops_list(request):
    """
        Endpoint for loading all workshops list (for AJAX)
    """
    workshops = Workshop.objects.filter(user=request.user).order_by('create_date').all()

    return render(
        request=request,
        template_name='include/workshops/modal_workshops_list.html',
        context={'workshops': workshops}
    )
