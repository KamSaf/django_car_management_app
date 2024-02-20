from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return render(request, 'cars/home.html')
    else:
        return redirect('welcome_page')
