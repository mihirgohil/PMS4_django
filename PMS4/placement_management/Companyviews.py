from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from placement_management.models import Companys

from placement_management.models import CustomUser


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


def post_internship(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/post_internship.html",context=context)


def working_internship(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/working_internship.html",context=context)


def history(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/history.html",context=context)


def company_logout(request):
    company_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": company_obj
    }
    return render(request, "company_template/company_logout.html")
