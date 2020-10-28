from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    # process function called when view is shown
    def process_view(self,request,view_func,view_args,view_kwargs):
        # it will get the module name means where the view is defined
        modulename=view_func.__module__
        # get user details
        user=request.user
        print(modulename)
        print(user)
        # check authentication
        if user.is_authenticated:
            print(request.user)

            # redirect according to their role
            if user.user_type == "1":
                if modulename == "placement_management.Collegeviews":
                    pass
                elif modulename == "placement_management.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("college"))
            elif user.user_type == "2":
                if modulename == "placement_management.Companyviews":
                    pass
                elif modulename == "placement_management.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("company"))
            elif user.user_type == "3":
                if modulename == "placement_management.Studentviews":
                    pass
                elif modulename == "placement_management.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student"))

            # if user authenticated but user type is not specified
            else:
                return HttpResponseRedirect(reverse("show_login"))
        else:
            print("user not authenticated")
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))