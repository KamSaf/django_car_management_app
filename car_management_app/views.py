from django.shortcuts import render, redirect
from workshops.forms import WorkshopForm
from workshops.models import Workshop


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
    return render(
        request=request,
        template_name='include/navbar.html',
        context={'user': request.user}
    )


def home(request):
    """
        View for rendering home page
    """
    workshops = Workshop.objects.filter(user=request.user).all()
    favourite_workshops = Workshop.objects.filter(user=request.user, favourite=True).order_by('last_edit_date').all()
    if request.user.is_authenticated:
        workshop_form = WorkshopForm(logged_user=request.user)
        return render(request, 'home.html', context={
            'new_workshop_form': workshop_form,
            'workshops': workshops,
            'favourite_workshops': favourite_workshops,
        })
    else:
        return redirect('welcome_page')
