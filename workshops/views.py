from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import WorkshopCreationForm
# from .models import Workshop


@api_view(['POST'])
@login_required
def async_add_workshop(request):
    """
        Endpoint for creating new workshop (for AJAX)
    """
    if request.method == 'POST':
        form = WorkshopCreationForm(request.POST, logged_user=request.user)
        form.clear_errors()
        if form.is_valid():
            form.save()
            return Response({'status': 'success'})
    return Response({
        'status': 'fail',
        'errors': form.data_errors,
    })
