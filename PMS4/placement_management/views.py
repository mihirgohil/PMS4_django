from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from placement_management.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import login_required
from placement_management.models import CustomUser


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
        user = auth.authenticate(request=request, username=request.POST.get("email"),
                                 password=request.POST.get("password"))
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
    if request.user is not None:
        return HttpResponse("User 1Email : " + request.user.email + " usertype :" + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def show_student_signup(request):
    return render(request, "student_signup.html")


def do_student_signup(request):
    enrolment_no = request.POST.get("enrolment_no")
    stu_name = request.POST.get("stu_name")
    username = request.POST.get("enrolment_no")
    email = request.POST.get("email")
    password = request.POST.get("password")
    dob = request.POST.get("dob")
    sex = request.POST.get("sex")
    phone_no = request.POST.get("phone_no")
    ssc_percentage = request.POST.get("ssc_percentage")
    hsc_percentage = request.POST.get("hsc_percentage")
    ug_stream = request.POST.get("ug_stream")
    ug_percentage = request.POST.get("ug_percentage")
    pg_cgpa = request.POST.get("pg_cgpa")
    print(enrolment_no)
    # try:
    #     profile_pic = request.FILES['profile_pic']
    #     fs = FileSystemStorage()
    #     filename = fs.save(profile_pic.name, profile_pic)
    #     profile_pic_url = fs.url(filename)
    # except MultiValueDictKeyError:
    #     is_private = False

    # try:
    user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=3)
    user.students.enrolment_no = enrolment_no
    user.students.stu_name = stu_name
    user.students.phone_no = phone_no
    user.students.gender = sex
    user.students.ssc_percentage = ssc_percentage
    user.students.hsc_percentage = hsc_percentage
    user.students.ug_stream = ug_stream
    user.students.ug_percentage = ug_percentage
    user.students.dob = dob
    user.students.pg_cgpa = pg_cgpa
    user.students.profile_pic = 'blank'
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    # except:
    #      messages.error(request, "Failed to Add Student")
    #      return HttpResponseRedirect(reverse("show_student_signup"))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")
