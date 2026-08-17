from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from guests.models import Guest
from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Guest.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
            )
            login(request, user)
            messages.success(request, "Welcome to Royal Stay Hotels! Your account has been created.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_staff else 'home')

    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if next_url:
                return redirect(next_url)
            return redirect('admin_dashboard' if user.is_staff else 'home')
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form, 'next': next_url})


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name or user.username}!")
                return redirect(next_url or 'admin_dashboard')
            else:
                form.add_error(None, "This account does not have staff access.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
