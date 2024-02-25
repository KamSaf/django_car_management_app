from django.shortcuts import render, redirect
from workshops.forms import WorkshopCreationForm
# from workshops.models import Workshop


# def home(request):
#     """
#         View for rendering home page
#     """
#     if request.user.is_authenticated:
#         workshop_form = WorkshopCreationForm(logged_user=request.user)
#         return render(request, 'cars/home.html', context={
#             'workshop_form': workshop_form
#         })
#     else:
#         return redirect('welcome_page')
