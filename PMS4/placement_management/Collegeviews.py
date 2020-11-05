from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# login required
from django.urls import reverse
from placement_management.models import PlacementDrives


def college_home(request):
    return render(request, "college_template/home_content.html")


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
            return HttpResponseRedirect("{% url 'add_new_pms_drive' %}")
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


# company pages
def add_company(request):
    return render(request, "college_template/add_company.html")


def manage_company(request):
    return render(request, "college_template/manage_company.html")


def add_student(request):
    return render(request, "college_template/add_student.html")


def manage_student(request):
    return render(request, "college_template/manage_student.html")


def student_feedback(request):
    return render(request, "college_template/student_feedback.html")


def company_feedback(request):
    return render(request, "college_template/company_feedback.html")


def college_logout(request):
    return render(request, "college_template/clg_logout.html")
