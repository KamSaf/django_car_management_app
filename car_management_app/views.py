from django.shortcuts import render


def welcome(request):
    return render(request, 'welcome.html')


def about(request):
    return render(request, 'about.html')
