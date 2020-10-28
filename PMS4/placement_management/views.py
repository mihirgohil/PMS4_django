from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from placement_management.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import login_required

# Create your views here.


def showDemoPage(request):
    return render(request, "demo.html")

# show login page
def showLoginPage(request):
    return render(request, "login_page.html")

# login logic
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        auth = EmailBackEnd()
        user = auth.authenticate(request=request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            # return HttpResponse("Email : " + request.POST.get("email") + " Password : " + request.POST.get("password"))
            if int(user.user_type) == 1:
                return HttpResponseRedirect('college')
            elif int(user.user_type) == 2:
                return HttpResponseRedirect('company')
            elif int(user.user_type) == 3:
                return HttpResponseRedirect('student')
            else:
                logout(request)
                messages.error(request, "Invalid User ")
                return HttpResponseRedirect('login')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect('login')

# showing base
def showBase(request):
    return render(request, "college_template/base_template.html")

# login required
@login_required(login_url='login')
def GetUserDetails(request):
    # return HttpResponse(request.is)
    if request.user != None:
         return HttpResponse("User 1Email : " + request.user.email + " usertype :" + request.user.user_type)
    else:
         return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")
