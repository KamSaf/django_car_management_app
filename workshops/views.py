from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import WorkshopForm
from .models import Workshop
from django.template.response import SimpleTemplateResponse



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

    return SimpleTemplateResponse(
        template='include/workshops/workshop_details.html',
        context={
            'workshop': workshop,
            'edit_workshop_form': form
        },
    )
