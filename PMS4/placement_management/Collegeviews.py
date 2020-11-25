from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# login required
from django.urls import reverse

from placement_management.utilty.choices import GENDER_CHOICES, UG_DEPARTMENTS_TYPE_SIGNUP,INVITE_MAIL_BODY


from django.core.files.storage import FileSystemStorage

from placement_management.models import CustomUser, Students, PlacementDrives, Companys

from placement_management.CollegeForms import PlacementcoordinatorForm
from placement_management.forms import StudentForm
from placement_management.forms import InternshipForm
from placement_management.utilty.utility_function import *


import random
import string
import json
#mail send
from django.core.mail import send_mail

from placement_management.models import InternshipDetails


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def college_home(request):
    return render(request, "college_template/home_content.html")

def add_new_placement_coordinator(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlacementcoordinatorForm(request.POST)
        context = {'form': form}
        # check whether it's valid:
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # obj = form.save(commit = False)
            password = str(get_random_alphanumeric_string(8))
            username = first_name+'-'+str(get_random_alphanumeric_string(3))
            # obj.password = password
            # obj.username = username
            # obj.user_type = 1
            # obj.save()
            CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                           email=email, password=password, user_type=1)

            subject = 'Account Created CPI Placement'
            message = 'Your Placement Coordinator Account Created on CPI Placement System By Admin.\nFor This Email Account.\nPassword : ' + password + '. \nYou can change the password from Profile.'
            from_email = 'placement@cpi.com'
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
            )
            messages.success(request,"Added New Placement Coordinator "+first_name)
            return HttpResponseRedirect(reverse('add_new_placement_coordinator'))

        else:
            messages.error(request, "With this email Account Already exists")
            return render(request, "college_template/add_new_placement_coordinator.html", {'form': form})
    else:
        form = PlacementcoordinatorForm()
        context = { 'form': form }
    return render(request, "college_template/add_new_placement_coordinator.html",context=context)

# placement drive related views
def add_new_placement_drive(request):
    return render(request, "college_template/add_new_placement_drive.html")


def add_new_placement_drive_save(request):
    if request.method == "POST":
        drive_name = request.POST.get("drive")
        try:
            drive_model = PlacementDrives(drive_name=drive_name)
            drive_model.save()
        except:
            messages.error(request, "Failed to Add Drive")
            return HttpResponseRedirect(reverse('add_new_pms_drive'))
        else:
            messages.success(request, "Drive Added : " + drive_name)
            return HttpResponseRedirect(reverse('clg_pmc_drive'))

    else:
        return HttpResponseRedirect("Method Not Allowed")


def placement_drive(request):
    placement_drives_list = PlacementDrives.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(placement_drives_list, 8)
    try:
        placement_drives = paginator.page(page)
    except PageNotAnInteger:
        placement_drives = paginator.page(1)
    except EmptyPage:
        placement_drives = paginator.page(paginator.num_pages)
    
    return render(request, "college_template/placement_drive.html", {"placement_drives": placement_drives})

def placement_invite_companies(request,drive_id):
    manage_company_list = Companys.objects.all().order_by('-created_at')
    drive_info = PlacementDrives.objects.get(id=drive_id)

    return render(request, "college_template/invite_companies_for_drive.html", {"companys": manage_company_list,"drive_info":drive_info})
def do_placement_invite_companies(request):
    drive_id = request.POST.get('drive_id')
    selected_companies = request.POST.get('input_hidden_field')
    selected_companies_list = json.loads(selected_companies)
    drive_info = PlacementDrives.objects.get(id=drive_id)

    subject = request.POST.get('subject')
    message = request.POST.get('mail_body')
    from_email = "mca@cpi.edu.in"
    send_mail(subject, message, from_email, selected_companies_list)
    messages.success(request, "Invite Send")
    return HttpResponseRedirect(reverse("pms_invite",kwargs={'drive_id':drive_id}))

## internship
def create_internship(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InternshipForm(request.POST)
        context = {'form': form}
        # check whether it's valid:
        if form.is_valid():
           # form.save()
           # print(form.cleaned_data['contact_person_name'])
           messages.success(request, "Internship Created ")
           return HttpResponseRedirect(reverse('clg_internship_create'))
        else:
            messages.success(request, "Internship Not Created ")
            render(request, "college_template/add_new_internship.html", {'form': form})
    else:
        form = InternshipForm()
        context = {'form': form}
        return render(request, "college_template/add_new_internship.html", context=context)

def manage_internship(request):
    placement_drives_list = PlacementDrives.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(placement_drives_list, 8)
    try:
        placement_drives = paginator.page(page)
    except PageNotAnInteger:
        placement_drives = paginator.page(1)
    except EmptyPage:
        placement_drives = paginator.page(paginator.num_pages)

    return render(request, "college_template/manageInternship.html", {"placement_drives": placement_drives})


def manage_internship_published(request,drive_id):
    internships = InternshipDetails.objects.all().filter(placementDrive_id=drive_id, is_completed=0,is_posted=1).select_related("company")
    drive_info = PlacementDrives.objects.get(id=drive_id)
    return render(request, "college_template/managePublished.html",{'drive_id':drive_id,'drive_info':drive_info,'internships':internships})

def internship_reg_deactive(request,post_id,drive_id):
    messages.success(request, "Company Account Created")
    return HttpResponseRedirect(reverse("clg_add_company",kwargs={'drive_id':drive_id}))


def manage_internship_publish(request,drive_id):
    internships = InternshipDetails.objects.all().filter(placementDrive_id=drive_id,is_completed=0,is_posted=0).select_related("company")
    drive_info = PlacementDrives.objects.get(id=drive_id)
    return render(request, "college_template/managePublish.html",{'drive_id':drive_id,'internships':internships,'drive_info':drive_info})


def close_internship(request,drive_id):
    internships = InternshipDetails.objects.all().filter(placementDrive_id=drive_id, is_completed=1).select_related("company")
    drive_info = PlacementDrives.objects.get(id=drive_id)
    return render(request, "college_template/closed_internship.html",{'drive_id':drive_id,'drive_info':drive_info,'internships':internships})


# company pages
def add_company(request,newContext={}):
    context = {}
    context.update(newContext)
    return render(request, "college_template/add_company.html",context=context)


def add_company_save(request):
     name = request.POST.get("name")
     address = request.POST.get("address")
     website = request.POST.get("website")
     email = request.POST.get("email")
     phone = request.POST.get("phone")
     password = str(get_random_alphanumeric_string(8))
     username = name + '-' + str(get_random_alphanumeric_string(3))
     context = {
         'name': name,
         'address': address,
         'website': website,
         'email': email,
         'phone': phone}
     if name == "" or address == "" or website == "" or email == "" or phone == "":
         messages.error(request, "fill all the details")
         response = add_company(request, context)
         return response
     usermailcheck = CustomUser.objects.filter(email=email).first()
     if usermailcheck != None:
         messages.error(request, "With this email Account is already Created Kindly login or use different mail id.")
         response = add_company(request, context)
         return response

     if request.FILES.get('profile_pic'):
         profile_pic = request.FILES.get('profile_pic')
         # dir_storage = '/media/student_media/profile_picture/' + enrolment_no
         fs = FileSystemStorage()
         filename = fs.save(profile_pic.name, profile_pic)
         print(filename)
         profile_pic_url = fs.url(filename)
     else:
         profile_pic_url = '/media/default_avtar/user.jpg'

     user = CustomUser.objects.create_user(username=username, first_name=name, last_name="",
                                      email=email, password=password, user_type=2)

     user.companys.address = address
     user.companys.website = website
     user.companys.email = email
     user.companys.phone_no = phone
     user.companys.company_logo = profile_pic_url
     user.save()
     subject = 'Your Account Created CPI Placement'
     message = 'Your Company Account Created on CPI Placement System By Admin.\nFor This Email Account.\nPassword : ' + password + '. \nYou can change the password from Profile.'
     from_email = 'placement@cpi.com'
     send_mail(
         subject,
         message,
         from_email,
         [email],
         fail_silently=False,
     )
     messages.success(request, "Company Account Created")
     return HttpResponseRedirect(reverse("clg_add_company"))

def manage_company(request):
    manage_company_list = Companys.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(manage_company_list, 8)
    try:
        companys = paginator.page(page)
    except PageNotAnInteger:
        companys = paginator.page(1)
    except EmptyPage:
        companys = paginator.page(paginator.num_pages)
    return render(request, "college_template/manage_company.html", {"companys": companys})

def edit_company(request,id):
    edit_company = Companys.objects.get(id = id)
    context = {
        'edit_company': edit_company,
    }
    return render(request, "college_template/edit_company.html", context=context)

def edit_company_save(request):
    id = request.POST.get("company_id")
    print(id)
    name = request.POST.get("name")
    address = request.POST.get("address")
    website = request.POST.get("website")
    phone = request.POST.get("phone")
    context = {
        'name': name,
        'address': address,
        'website': website,
        'phone': phone}
    if name == "" or address == "" or website == "" or phone == "":
        messages.error(request, "fill all the details")
        response = edit_company(request,id)
        return response

    user = Companys.objects.get(id=id)
    if request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')
        # dir_storage = '/media/student_media/profile_picture/' + enrolment_no
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        print(filename)
        profile_pic_url = fs.url(filename)
        user.company_logo = profile_pic_url

    usertable = CustomUser.objects.get(id = user.user_type_id)
    usertable.first_name = name
    usertable.save()
    user.address = address
    user.website = website
    user.phone_no = phone
    user.save()
    messages.success(request, "Company Account Updated")
    return HttpResponseRedirect(reverse("clg_edit_company",kwargs={'id':id}))


def add_student(request,newContext={}):
    drive = PlacementDrives.objects.filter(is_completed=0)
    context = {
        "gender": GENDER_CHOICES,
        "ug_dept_type": UG_DEPARTMENTS_TYPE_SIGNUP,
        "drive": drive,
    }
    context.update(newContext)
    return render(request, "college_template/add_student.html",context)

def add_student_save(request):
    enrolment_no = request.POST.get("enrolment_no")
    stu_first_name = request.POST.get("stu_first_name")
    stu_last_name = request.POST.get("stu_last_name")
    username = request.POST.get("enrolment_no")
    email = request.POST.get("email")
    dob = request.POST.get("dob")
    sex = request.POST.get("sex")
    phone_no = request.POST.get("phone_no")
    ssc_percentage = request.POST.get("ssc_percentage")
    hsc_percentage = request.POST.get("hsc_percentage")
    ug_stream = request.POST.get("ug_stream")
    ug_percentage = request.POST.get("ug_percentage")
    pg_cgpa = request.POST.get("pg_cgpa")
    drive = request.POST.get("drive")

    password = str(get_random_alphanumeric_string(8))

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
        response = add_student(request, context)
        return response

    if drive == "default_drive":
        messages.error(request, "invalid drive")
        response = add_student(request, context)
        return response

    if sex == "Select_Gender":
        messages.error(request, "invalid gender")
        response = add_student(request, context)
        return response

    if ug_stream == "Select_ug_stream":
        messages.error(request, "invalid ug stream")
        response = add_student(request, context)
        return response

    if request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')
        # dir_storage = '/media/student_media/profile_picture/' + enrolment_no
        fs = FileSystemStorage()
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

        response = add_student(request, context)
        return response
    if usernamecheck != None:
        messages.error(request, "With this enrollment Account is already Created")
        response = add_student(request, context)
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
    subject = 'Account Created CPI Placement'
    message = 'Your Student Account Created on CPI Placement System By Admin.\nFor This Email Account.\nPassword : '+ password +'. \nYou can change the password from Profile.'
    from_email = 'placement@cpi.com'
    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )
    messages.success(request, "Student Account Created")
    return HttpResponseRedirect(reverse("clg_add_student"))


def manage_student(request):
    placement_drives_list = PlacementDrives.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(placement_drives_list, 8)
    try:
        placement_drives = paginator.page(page)
    except PageNotAnInteger:
        placement_drives = paginator.page(1)
    except EmptyPage:
        placement_drives = paginator.page(paginator.num_pages)
    return render(request, "college_template/manage_student.html",  {"placement_drives": placement_drives})

def show_Studentlist(request,drive_id):
    show_student_list = Students.objects.filter(placementDrive_id = drive_id).order_by('-created_at')
    drive_info = PlacementDrives.objects.get(id=drive_id)
    print(drive_info)
    page = request.GET.get('page', 1)
    paginator = Paginator(show_student_list, 8)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    return render(request, "college_template/show_Studentlist.html",  {"students": students,"drive_info":drive_info})

def edit_student(request,id):
    edit_student = Students.objects.get(id=id)
    context = {
        'edit_student': edit_student,
    }
    return render(request, "college_template/edit_student.html", context=context)


def edit_student_save(request):
    id = request.POST.get("student_id")
    print(id)
    enrolment_no = request.POST.get("enrolment_no")
    stu_first_name = request.POST.get("stu_first_name")
    stu_last_name = request.POST.get("stu_last_name")
    sex = request.POST.get("sex")
    phone_no = request.POST.get("phone_no")
    ssc_percentage = request.POST.get("ssc_percentage")
    hsc_percentage = request.POST.get("hsc_percentage")
    ug_stream = request.POST.get("ug_stream")
    ug_percentage = request.POST.get("ug_percentage")
    pg_cgpa = request.POST.get("pg_cgpa")


    context = {
        "eno": enrolment_no,
        "fname": stu_first_name,
        "lname": stu_last_name,
        "phone_no": phone_no,
        "ssc": ssc_percentage,
        "hsc": hsc_percentage,
        "ug": ug_percentage,
        "pg": pg_cgpa,
    }

    if enrolment_no == "" or stu_first_name == "" or stu_last_name == "" or phone_no == "" or ssc_percentage == "" or hsc_percentage == "" or ug_stream == "" or ug_percentage == "" or pg_cgpa == "":
        messages.error(request, "fill all the details")
        response = edit_student(request, context)
        return response

    user = Students.objects.get(id=id)
    if request.FILES.get('profile_pic'):
        profile_pic = request.FILES.get('profile_pic')
        # dir_storage = '/media/student_media/profile_picture/' + enrolment_no
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        print(filename)
        profile_pic_url = fs.url(filename)
        user.profile_pic = profile_pic_url

    # usernamecheck = CustomUser.objects.filter(username=enrolment_no).first()
    #
    # if usernamecheck != None:
    #     messages.error(request, "With this enrollment Account is already Created")
    #     response = edit_student(request, context)
    #     return response

    usertable = CustomUser.objects.get(id=user.user_type_id)
    usertable.first_name = stu_first_name
    usertable.last_name = stu_last_name
    usertable.save()
    user.enrolment_no = enrolment_no
    user.gender = sex
    user.phone_no = phone_no
    user.ssc_percentage = ssc_percentage
    user.hsc_percentage = hsc_percentage
    user.ug_percentage = ug_percentage
    user.pg_cgpa = pg_cgpa
    user.save()

    messages.success(request, "Student Account Updated")
    return HttpResponseRedirect(reverse("clg_edit_student", kwargs={'id': id}))


def student_feedback(request):
    return render(request, "college_template/student_feedback.html")


def company_feedback(request):
    return render(request, "college_template/company_feedback.html")


def college_logout(request):
    return render(request, "college_template/clg_logout.html")

