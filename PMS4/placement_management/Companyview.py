from django.shortcuts import render


def company_home(request):
    return render(request, "company_template/home_content.html")


def company_profile(request):
    return render(request, "company_template/company_profile.html")


def post_internship(request):
    return render(request, "company_template/post_internship.html")


def working_internship(request):
    return render(request, "company_template/working_internship.html")


def history(request):
    return render(request, "company_template/history.html")


def company_logout(request):
    return render(request, "company_template/company_logout.html")
