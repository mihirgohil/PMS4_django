from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from placement_management.models import CustomUser, Students, PlacementDrives, Companys, InternshipDetails, StudentAppliedForInternships


def company_home(request):
    student_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": student_obj
    }
    return render(request, "company_template/home_content.html", context)


def company_profile(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/company_profile.html", context=context)

def company_profile_edit(request,id):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/company_profile_edit.html", context=context)

def company_profile_editSave(request):
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
        response = company_profile_edit(request, id)
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

    usertable = CustomUser.objects.get(id=user.user_type_id)
    usertable.first_name = name
    usertable.save()
    user.address = address
    user.website = website
    user.phone_no = phone
    user.save()
    messages.success(request, "Company Account Updated")
    return HttpResponseRedirect(reverse("company_profile_edit", kwargs={'id': id}))


def post_internship(request,newContext={}):
    company_obj = Companys.objects.get(user_type=request.user.id)
    placement_drive_list = PlacementDrives.objects.filter(is_completed=0)
    context = {
        "company_obj": company_obj,
        'placement_drive_list': placement_drive_list,
    }
    return render(request, "company_template/post_internship.html",context=context)


def post_internship_save(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    if request.method == "POST":
        placementDrive_id = request.POST.get("placementDrive_id")
        contact_person_names = request.POST.get("contact_person_names")
        designation = request.POST.get("designation")
        contact_person_numbers = request.POST.get("contact_person_numbers")
        contact_person_emails = request.POST.get("contact_person_emails")
        company_brief_overview =request.POST.get("company_brief_overview")
        number_of_positions = request.POST.get("number_of_positions")
        internship_duration = request.POST.get("internship_duration")
        recruitment_process = request.POST.get("recruitment_process")
        mode_of_interview = request.POST.get("mode_of_interview")
        working_hours = request.POST.get("working_hours")
        stipend_per_month = request.POST.get("stipend_per_month")
        ctc = request.POST.get("ctc")
        bond_details =request.POST.get("bond_details")
        intern_obj = InternshipDetails()
        intern_obj.company = company_obj
        intern_obj.placementDrive = PlacementDrives.objects.get(id=placementDrive_id)
        intern_obj.contact_person_names = contact_person_names
        intern_obj.designation = designation
        intern_obj.contact_person_numbers = contact_person_numbers
        intern_obj.contact_person_emails = contact_person_emails
        intern_obj.company_breaf_overview = company_brief_overview
        intern_obj.number_of_positions = number_of_positions
        intern_obj.internship_duration = internship_duration
        intern_obj.recruitment_process = recruitment_process
        intern_obj.mode_of_interview = mode_of_interview
        intern_obj.working_hours = working_hours
        intern_obj.stipend_per_month = stipend_per_month
        intern_obj.ctc = ctc
        intern_obj.bond_details = bond_details
        intern_obj.save()
        messages.success(request, "Internship Job Created")
        return HttpResponseRedirect(reverse("company_post_job"))
    else:
        context = {}
        messages.error(request, "Method Not Allowed")
        response = post_internship(request, context)
        return response

def post_internship_edit(request,post_id):
    internship = InternshipDetails.objects.get(id=post_id)
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj,
        'edit_internship' : internship,
        'post_id' : post_id,
    }
    return render(request, "company_template/company_edit_internship.html", context=context)

def post_internship_edit_save(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        contact_person_names = request.POST.get("contact_person_names")
        designation = request.POST.get("designation")
        contact_person_numbers = request.POST.get("contact_person_numbers")
        contact_person_emails = request.POST.get("contact_person_emails")
        company_breaf_overview =request.POST.get("company_breaf_overview")
        number_of_positions = request.POST.get("number_of_positions")
        internship_duration = request.POST.get("internship_duration")
        recruitment_process = request.POST.get("recruitment_process")
        mode_of_interview = request.POST.get("mode_of_interview")
        working_hours = request.POST.get("working_hours")
        stipend_per_month = request.POST.get("stipend_per_month")
        ctc = request.POST.get("ctc")
        bond_details =request.POST.get("bond_details")
        intern_obj = InternshipDetails.objects.get(id=post_id)
        intern_obj.contact_person_names = contact_person_names
        intern_obj.designation = designation
        intern_obj.contact_person_numbers = contact_person_numbers
        intern_obj.contact_person_emails = contact_person_emails
        intern_obj.company_breaf_overview = company_breaf_overview
        intern_obj.number_of_positions = number_of_positions
        intern_obj.internship_duration = internship_duration
        intern_obj.recruitment_process = recruitment_process
        intern_obj.mode_of_interview = mode_of_interview
        intern_obj.working_hours = working_hours
        intern_obj.stipend_per_month = stipend_per_month
        intern_obj.ctc = ctc
        intern_obj.bond_details = bond_details
        intern_obj.save()
        messages.success(request, "Internship Job Edited")
        return HttpResponseRedirect(reverse("company_working_job"))
    else:
        messages.error(request, "Method Not Allowed")
        return HttpResponseRedirect(reverse("company_working_job"))



def working_internship(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    internships = InternshipDetails.objects.all().filter(company_id=company_obj.id, is_completed=0).select_related("company").order_by('-id')
    context = {
        "company_obj": company_obj,
        'internships': internships
    }
    return render(request, "company_template/working_internship.html",context=context)

def company_student_applied_for_internship_working(request,post_id):
    company_obj = Companys.objects.get(user_type=request.user.id)
    selected_internship = StudentAppliedForInternships.objects.filter(internship_id = post_id)
    internship = InternshipDetails.objects.get(id=post_id)
    context = {
        "company_obj": company_obj,
        "internship" : internship,
        "selected_internship": selected_internship
    }
    return render(request, "company_template/company_student_applied_for_working_internship.html",context=context)

def company_internship_close(request,post_id):
    company_obj = Companys.objects.get(user_type=request.user.id)
    internship = InternshipDetails.objects.get(id=post_id)
    internship.is_completed = 1
    internship.save()
    return HttpResponseRedirect(reverse("company_working_job"))

def history(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    internships = InternshipDetails.objects.all().filter(company_id=company_obj.id, is_completed=1).select_related("company").order_by('-id')
    context = {
        "company_obj": company_obj,
        'internships': internships
    }
    return render(request, "company_template/history.html",context=context)

def company_student_applied_for_internship_closed(request,post_id):
    company_obj = Companys.objects.get(user_type=request.user.id)
    selected_internship = StudentAppliedForInternships.objects.filter(internship_id = post_id)
    internship = InternshipDetails.objects.get(id=post_id)
    context = {
        "company_obj": company_obj,
        "internship" : internship,
        "selected_internship": selected_internship
    }
    return render(request, "company_template/company_student_applied_for_closed_internship.html",context=context)


def company_logout(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/company_logout.html")
