from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
            print(f'\n\n\n\n {User.objects.get(email=form.cleaned_data.get("email"))} \n\n\n ')
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
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        form.clear_errors()
        if form.is_valid():
            form.save()
            messages.success(request, 'Account data edited!')
            redirect('profile_page')
        else:
            for error in form.data_errors:
                messages.error(request, error)
    else:
        form = UserUpdateForm()
    if request.user:
        form = form.set_initial(user=request.user)
    return render(request=request, template_name='users/profile.html', context={'form': form})


@login_required
def delete_user(request):
    """
        Endpoint for deleting (deactivating) User
    """
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    user.save()
    return redirect('welcome_page')


@login_required
def edit_user(request):
    """
        Endpoint for editing User data (for AJAX)
    """
    return redirect('profile_page')
