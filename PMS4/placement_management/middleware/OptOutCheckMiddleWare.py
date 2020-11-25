from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from placement_management.models import Students, StudentOptOut
class OptOutCheckMiddleWare(MiddlewareMixin):

    # process function called when view is shown
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if user.is_authenticated:
            print(request.user)
            if user.user_type == "3":
                print("optout")
                if user.students.is_optout:

                    student_obj = StudentOptOut.objects.get(student_id=user.students.id)
                    context = {
                        "student_obj": student_obj
                    }
                    return render(request, "student_template/optout_home.html", context)