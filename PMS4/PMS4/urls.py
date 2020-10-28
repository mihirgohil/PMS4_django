"""PMS4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from placement_management import views, Collegeviews, Studentviews, Companyview

urlpatterns = [
    path('demo', views.showDemoPage),
    path('admin/', admin.site.urls),
    # login
    path('', views.showLoginPage),
    path('login', views.showLoginPage, name="login"),
    path('doLogin', views.doLogin),
    # get user details
    path('get_user_details', views.GetUserDetails),
    # logout
    path('logout', views.logout_user, name='logout'),
    # pms links
    path('pms/', include('placement_management.urls', namespace="pms")),
    # College Paths
    path('college/', Collegeviews.college_home, name="college"),
    path('college/add_company', Collegeviews.add_company, name="clg_add_company"),
    path('college/add_student', Collegeviews.add_student, name="clg_add_student"),
    path('college/manage_student', Collegeviews.manage_student, name="clg_manage_student"),
    path('college/manage_company', Collegeviews.manage_company, name="clg_manage_company"),
    path('college/placement_drive', Collegeviews.placement_drive, name="clg_pmc_drive"),
    path('college/student_feedback', Collegeviews.student_feedback, name="clg_student_feedback"),
    path('college/company_feedback', Collegeviews.company_feedback, name="clg_company_feedback"),
    # Student Paths
    path('student/', Studentviews.student_home, name="student"),
    path('streams', Studentviews.streams),
    path('stu_profile', Studentviews.stu_profile),
    path('apply_internship', Studentviews.apply_internship),
    path('opt_out', Studentviews.opt_out),
    path('stu_logout', Studentviews.stu_logout),
    # Company paths
    path('company/', Companyview.company_home, name="company"),
    path('company_profile', Companyview.company_profile),
    path('post_internship', Companyview.post_internship),
    path('working_internship', Companyview.working_internship),
    path('history', Companyview.history),
    path('company_logout', Companyview.company_logout),
]
