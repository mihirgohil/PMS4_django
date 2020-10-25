from django.shortcuts import render


def college_home(request):
    return render(request, "college_template/home_content.html")


def add_company(request):
    return render(request, "college_template/add_company.html")


def manage_company(request):
    return render(request, "college_template/manage_company.html")


def add_student(request):
    return render(request, "college_template/add_student.html")


def manage_student(request):
    return render(request, "college_template/manage_student.html")


def placement_drive(request):
    return render(request, "college_template/placement_drive.html")


def student_feedback(request):
    return render(request, "college_template/student_feedback.html")


def company_feedback(request):
    return render(request, "college_template/company_feedback.html")
