from django.shortcuts import render,redirect
from user.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def userLogin(request,*arg,**kwargs):

    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate( username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('quiz/')
    context = {}
    return render(request,'user/index.html',context)

def logOutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request,*arg,**kwargs):
    
    if request.method == "POST": 
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {
        'form':form
    
    }
    return render(request,'user/register.html',context)


