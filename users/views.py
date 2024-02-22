from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view


def register(request):
    """
        View rendering User registration page
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            auth_login(request, User.objects.get(email=form.cleaned_data.get('email')))
            return redirect('home_page')
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='users/register.html', context={'form': form})


@login_required
def user_profile(request):
    """
        View rendering User account information page
    """
    # if request.method == 'POST':
    #     form = UserUpdateForm(request.POST, instance=request.user)
        # form.clear_errors()
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Account data edited!')
    #         redirect('profile_page')
    #     else:
    #         for error in form.data_errors:
    #             messages.error(request, error)
    # else:
    form = UserUpdateForm()
    if request.user:
        form = form.set_initial(user=request.user)
    return render(request=request, template_name='users/profile.html', context={'form': form, 'cars_number': 3})


@login_required
def delete_user(request):
    """
        Endpoint for deleting (deactivating) User
    """
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.is_active = False
        user.save()
    return redirect('welcome_page')


@api_view(['POST'])
@login_required
def async_edit_user(request):
    """
        Endpoint for editing User data (for AJAX)
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        form.clear_errors()
        if form.is_valid():
            # form.save()
            return Response({
                'status': 'success',
                'email': form.cleaned_data.get('email'),
                'name': form.cleaned_data.get('name'),
                'username': form.cleaned_data.get('username'),
            })
    return Response({
        'status': 'fail',
        'errors': form.data_errors,
    })
