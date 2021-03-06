from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth

from production.decorators import  unauthenticated_user

# Create your views here.
@unauthenticated_user
def login(request):
    if (request.method=="POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if  user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('maintenance:machines')
        else:
            messages.error(request, "Wrong username or password")
            return redirect('accounts:login')

    else:
        return render(request, "accounts/login.html")

def register_user_page(request):
    return render(request, "accounts/register.html")


def register_user(request):
    if (request.method == "POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, "This username is taken")
                return redirect('accounts:register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, "This email is taken")
                    return redirect('accounts:register')
                else:
                    # save user details
                    user = User.objects.create_user(username=username, 
                                        first_name=first_name,
                                        last_name=last_name, email=email, 
                                        password=password)
                    auth.login(request, user)
                    messages.success(request, "You are now registered and can now login")
                    return redirect("accounts:login")

        else:
            messages.error(request, 'Passwords do not match')
            return redirect("accounts:register")

def logout_view(request):
    auth.logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('accounts:login')

@unauthenticated_user
def profile(request):
    return render(request, "accounts/profile.html")


def landing_page(request):
    return render(request, "accounts/landing_page.html")



# Accounts used
# last_name name Lamunu
# first_name Gloria 
# email labae@gmail.com
#  username la
# password anadol4567


# first_name: Arnold
# password: checkmate345