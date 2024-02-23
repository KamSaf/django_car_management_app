from django.shortcuts import render
from django.template.response import SimpleTemplateResponse


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
