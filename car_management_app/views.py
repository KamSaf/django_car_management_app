from django.shortcuts import render, redirect
from django.template.response import SimpleTemplateResponse
from workshops.forms import WorkshopForm
from workshops.models import Workshop
from django.utils import timezone


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
    workshops = Workshop.objects.filter(user=request.user).all()
    if request.user.is_authenticated:
        workshop_form = WorkshopForm(logged_user=request.user)
        return render(request, 'home.html', context={
            'workshop_form': workshop_form,
            'workshops': workshops,
        })
    else:
        return redirect('welcome_page')
