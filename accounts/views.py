from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context = {}

        if User.objects.filter(username=username).exists():
            context['username_taken'] = True  # <-- match template
            return render(request, 'accounts/register.html', context)

        if User.objects.filter(email=email).exists():
            context['email_taken'] = True  # <-- match template
            return render(request, 'accounts/register.html', context)

        if password != confirm_password:
            context['password_mismatch'] = True
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('default')
        else:
            return render(request, 'accounts/login.html', {'invalid_login': True})

    return render(request, 'accounts/login.html')
