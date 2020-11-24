from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import os
from django.utils.datastructures import MultiValueDictKeyError
from placement_management.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import login_required
from placement_management.models import CustomUser, Students
from placement_management.utilty.choices import GENDER_CHOICES, UG_DEPARTMENTS_TYPE_SIGNUP

from django_email_verification import sendConfirm

# Create your views here.
from PMS4 import settings
from placement_management.models import PlacementDrives


def showDemoPage(request):
    return render(request, "demo.html")


# show login page
def showLoginPage(request, newContext={}):
    context = {}
    context.update(newContext)
    if request.user.is_authenticated:
        print("Logged in")
        if int(request.user.user_type) == 1:
            return HttpResponseRedirect('college')
        elif int(request.user.user_type) == 2:
            return HttpResponseRedirect('company')
        elif int(request.user.user_type) == 3:
            return HttpResponseRedirect('student')
    return render(request, "login_page.html", context)


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
            email = request.POST.get("email")
            messages.error(request, "Invalid Login Details")
            context = {
                "email": email
            }
            response = showLoginPage(request, context)
            return response


# showing base
def showBase(request):
    return render(request, "college_template/base_template.html")


# login required
@login_required(login_url='login')
def GetUserDetails(request):
    # return HttpResponse(request.is)
    if request.user is not None:
        return HttpResponse("User Email : " + request.user.email + " usertype :" + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def show_student_signup(request, newContext={}):
    drive = PlacementDrives.objects.filter(is_completed=0)
    context = {
        "gender": GENDER_CHOICES,
        "ug_dept_type": UG_DEPARTMENTS_TYPE_SIGNUP,
        "drive": drive,
    }
    context.update(newContext)
    return render(request, "student_signup.html", context)


def do_student_signup(request):
    enrolment_no = request.POST.get("enrolment_no")
    stu_first_name = request.POST.get("stu_first_name")
    stu_last_name = request.POST.get("stu_last_name")
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
    drive = request.POST.get("drive")

    context = {
        "eno": enrolment_no,
        "fname": stu_first_name,
        "lname": stu_last_name,
        "email": email,
        "dob": dob,
        "phone_no": phone_no,
        "ssc": ssc_percentage,
        "hsc": hsc_percentage,
        "ug": ug_percentage,
        "pg": pg_cgpa,
    }

    if enrolment_no == "" or stu_first_name == "" or stu_last_name == "" or email == "" or password == "" or dob == "" or phone_no == "" or ssc_percentage == "" or hsc_percentage == "" or ug_stream == "" or ug_percentage == "" or pg_cgpa == "":
        messages.error(request, "fill all the details")
        response = show_student_signup(request, context)
        return response

    if drive == "default_drive":
        messages.error(request, "invalid drive")
        response = show_student_signup(request, context)
        return response

    if sex == "Select_Gender":
        messages.error(request, "invalid gender")
        response = show_student_signup(request, context)
        return response

    if ug_stream == "Select_ug_stream":
        messages.error(request, "invalid ug stream")
        response = show_student_signup(request, context)
        return response

    if request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')
        dir_storage = '/media/student_media/profile_picture/' + enrolment_no
        fs = FileSystemStorage(location=dir_storage , base_url = dir_storage)
        filename = fs.save(profile_pic.name, profile_pic)
        print(filename)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url = '/media/default_avtar/user.jpg'

    # try:
    usermailcheck = CustomUser.objects.filter(email=email).first()
    usernamecheck = CustomUser.objects.filter(username=enrolment_no).first()
    if usermailcheck != None:
        messages.error(request, "With this email Account is already Created Kindly login or use different mail id.")
        # return HttpResponseRedirect(reverse("show_student_signup"))

        response = show_student_signup(request, context)
        return response
    if usernamecheck != None:
        messages.error(request, "With this enrollment Account is already Created")
        response = show_student_signup(request, context)
        return response

    user = CustomUser.objects.create_user(username=username, first_name=stu_first_name, last_name=stu_last_name,
                                          email=email, password=password, user_type=3)
    user.students.phone_no = phone_no
    user.students.enrolment_no = enrolment_no
    user.students.gender = sex
    user.students.ssc_percentage = ssc_percentage
    user.students.hsc_percentage = hsc_percentage
    user.students.ug_stream = ug_stream
    user.students.ug_percentage = ug_percentage
    user.students.dob = dob
    user.students.pg_cgpa = pg_cgpa
    user.students.placementDrive_id = drive
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Student Account Created Login")
    return HttpResponseRedirect(reverse("login"))
    # except  Exception:
    #     messages.error(request, "Failed to Add Student")
    #     response = show_student_signup(request, context)
    #     return response


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")
