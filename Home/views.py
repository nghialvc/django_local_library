from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def loginview(request):
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return render(request,'home/login.html',{'form':form,'error':'Your username or password is incorrect!'})
    return render(request,'home/login.html',{'form':form,'error':''})
