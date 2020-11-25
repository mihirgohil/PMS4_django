from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from placement_management.models import CustomUser, Students, PlacementDrives, Companys, InternshipDetails, StudentOptOut


def student_home(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    drive_id = student_obj.placementDrive_id
    internships = InternshipDetails.objects.all().filter(placementDrive_id=drive_id,is_completed=0,is_posted=1).select_related("company").order_by('-id')
    context = {
        "student_obj": student_obj,
        'internships': internships
    }
    return render(request, "student_template/home_content.html", context)


def feeds(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/feeds.html", context)


def stu_profile(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/stu_profile.html", context)


def stu_profile_edit(request,id):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/stu_profile_edit.html", context)


def stu_profile_edit_save(request):
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
        response = stu_profile(request, context)
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
    return HttpResponseRedirect(reverse("stu_profile_edit", kwargs={'id': id}))


def apply_internship(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/apply_internship.html", context)


def opt_out(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/opt_out.html", context)

def opt_out_save(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    student_obj.is_optout = 1
    student_obj.save()
    optout = StudentOptOut()
    optout.student = student_obj
    optout.title = request.POST.get('title')
    optout.reason = request.POST.get('optout')
    optout.save()
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/optout_home.html", context)

def stu_logout(request):
    return render(request, "student_template/stu_logout.html")
