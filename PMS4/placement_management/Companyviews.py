from django.shortcuts import render

from placement_management.models import Companys

def company_home(request):
    student_obj = Companys.objects.get(user_type=request.user.id)
    context = {
        "company_obj": student_obj
    }
    return render(request, "company_template/home_content.html", context)


def company_profile(request):
    company_obj = Companys.objects.all()
    context = {
        "company": company_obj
    }
    return render(request, "company_template/company_profile.html", context=context)


def post_internship(request):
    return render(request, "company_template/post_internship.html")


def working_internship(request):
    return render(request, "company_template/working_internship.html")


def history(request):
    return render(request, "company_template/history.html")


def company_logout(request):
    return render(request, "company_template/company_logout.html")
