from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login # in-built authentication framework
from django.contrib.auth.views import LoginView,LogoutView
from .forms import LoginForm

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username = cd['username'],password = cd['password']) # returns User object if the user exists else None
            if user is not None:
                if user.is_active:
                    login(request,user) # sets the user into a session 
                    return HttpResponse("Authenticated successfully")
                else: 
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login') # if user does not exist
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form}) # pass the form data to the html file


# Create your views here.
