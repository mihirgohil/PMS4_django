from django.shortcuts import render

from placement_management.models import Students


def student_home(request):
    print("kko")
    print(request.user.id)
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/home_content.html", context)


def feeds(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/feeds.html",context)


def stu_profile(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/stu_profile.html",context)


def apply_internship(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/apply_internship.html",context)


def opt_out(request):
    student_obj = Students.objects.get(user_type=request.user.id)
    context = {
        "student_obj": student_obj
    }
    return render(request, "student_template/opt_out.html",context)


def stu_logout(request):
    return render(request, "student_template/stu_logout.html")
