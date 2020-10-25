from django.shortcuts import render


def student_home(request):
    return render(request, "student_template/home_content.html")


def streams(request):
    return render(request, "student_template/streams.html")


def stu_profile(request):
    return render(request, "student_template/stu_profile.html")


def apply_internship(request):
    return render(request, "student_template/apply_internship.html")


def opt_out(request):
    return render(request, "student_template/opt_out.html")


def stu_logout(request):
    return render(request, "student_template/stu_logout.html")
