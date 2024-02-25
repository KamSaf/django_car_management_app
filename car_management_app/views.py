from django.shortcuts import render, redirect
from django.template.response import SimpleTemplateResponse
from workshops.forms import WorkshopCreationForm


def welcome(request):
    """
        View rendering welcome page
    """
    return render(request, 'welcome.html')


def about(request):
    """
        View rendering about page with app and author contact info
    """
    return render(request, 'about.html')


def refresh_navbar(request):
    """
        Endpoint returnig navbar template (for AJAX navbar refresh)
    """
    return SimpleTemplateResponse('include/navbar.html', context={'user': request.user})


def home(request):
    """
        View for rendering home page
    """
    if request.user.is_authenticated:
        workshop_form = WorkshopCreationForm(logged_user=request.user)
        return render(request, 'home.html', context={
            'workshop_form': workshop_form
        })
    else:
        return redirect('welcome_page')
