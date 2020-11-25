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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

from placement_management import views, Collegeviews, Studentviews, Companyviews


from PMS4 import settings

urlpatterns = [
    path('demo', views.showDemoPage),
    path('student_signup', views.show_student_signup, name="show_student_signup"),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    # login
    path('', views.showLoginPage,name="show_login"),
    path('login', views.showLoginPage, name="login"),
    path('doLogin', views.doLogin,name="do_login"),
    path('do_student_signup', views.do_student_signup, name="do_student_signup"),
    # get user details
    path('get_user_details', views.GetUserDetails),
    # logout
    path('logout', views.logout_user, name='logout'),
    # pms links
    path('pms/', include('placement_management.urls', namespace="pms")),
    # College Paths
    path('college', Collegeviews.placement_drive, name="college"),
    # ## Add new Placement Coordinator
    path('college/add_new_placement_coordinator', Collegeviews.add_new_placement_coordinator, name="add_new_placement_coordinator"),
    # ##       placement drive related pages
    path('college/placement_drive', Collegeviews.placement_drive, name="clg_pmc_drive"),
    path('college/add_new_placement_drive', Collegeviews.add_new_placement_drive, name="add_new_pms_drive"),
    path('college/add_new_placement_drive_save', Collegeviews.add_new_placement_drive_save, name="add_new_pms_save"),
    path('college/add_new_placement_drive_invite_companies/<drive_id>',Collegeviews.placement_invite_companies, name="pms_invite"),
    path('college/do_add_new_placement_drive_invite_companies',Collegeviews.do_placement_invite_companies, name="do_pms_invite"),
    # ##
    path('college/add_company', Collegeviews.add_company, name="clg_add_company"),
    path('college/add_company/save', Collegeviews.add_company_save, name="clg_add_company_save"),

    path('college/add_student', Collegeviews.add_student, name="clg_add_student"),
    path('college/add_student_save', Collegeviews.add_student_save, name="clg_add_student_save"),

    # ## Internship related page
    path('college/magage_internship_create',Collegeviews.create_internship,name="clg_internship_create"),
    path('college/magage_internship_create_save',Collegeviews.create_internship_save,name="clg_internship_create_save"),
    path('college/manage_internship', Collegeviews.manage_internship, name="clg_manage_internship"),
    path('college/manage_internship_publised/<drive_id>', Collegeviews.manage_internship_published, name="clg_manage_internship_published"),
    path('college/manage_internship_publish/<drive_id>', Collegeviews.manage_internship_publish,name="clg_manage_internship_publish"),
    path('college/close_internship/<drive_id>', Collegeviews.close_internship,name="clg_close_internship"),
    path('college/deactive_reg/<post_id>',Collegeviews.internship_reg_deactive,name="clg_close_internship_deactive"),
    path('college/edit_internship/<id>', Collegeviews.edit_internship, name="clg_edit_internship"),
    path('college/edit_internship_save', Collegeviews.edit_internship_save, name="clg_edit_internship_save"),

    path('college/internship_publish_to_student/<post_id>', Collegeviews.clg_publish_internship_update, name="clg_publish_internship_update"),

    path('college/internship_disable_reg_of_student/<post_id>', Collegeviews.clg_published_disable_reg_of_student, name="clg_published_disable_reg_of_student"),
    path('college/internship_enable_reg_of_student/<post_id>', Collegeviews.clg_published_enable_reg_of_student, name="clg_published_enable_reg_of_student"),


    # ## Manage Student
    path('college/manage_student', Collegeviews.manage_student, name="clg_manage_student"),
    path('college/show_student_list/<drive_id>', Collegeviews.show_Studentlist, name="clg_show_student"),
    path('college/placed_student_list/<drive_id>', Collegeviews.placed_Studentlist, name="clg_placed_student"),
    path('college/unplaced_student_list/<drive_id>', Collegeviews.unplaced_Studentlist, name="clg_unplaced_student"),

    path('college/edit_student/<id>', Collegeviews.edit_student, name="clg_edit_student"),
    path('college/edit_student_save', Collegeviews.edit_student_save, name="clg_edit_student_save"),


    # ## Manage Company
    path('college/manage_company', Collegeviews.manage_company, name="clg_manage_company"),
    path('college/edit_company/<id>', Collegeviews.edit_company, name="clg_edit_company"),
    path('college/edit_company_save', Collegeviews.edit_company_save, name="clg_edit_company_save"),

    path('college/student_feedback', Collegeviews.student_feedback, name="clg_student_feedback"),
    path('college/company_feedback', Collegeviews.company_feedback, name="clg_company_feedback"),

    # Student Paths
    path('student/', Studentviews.student_home, name="student"),
    path('student/feeds', Studentviews.feeds, name="stu_feeds"),

    #Manage Student Profile
    path('student/stu_profile', Studentviews.stu_profile, name="stu_profile"),
    path('student/stu_profile/edit/<id>', Studentviews.stu_profile_edit, name="stu_profile_edit"),
    path('student/stu_profile_editsave', Studentviews.stu_profile_edit_save, name="stu_profile_edit_save"),

    path('student/apply_internship', Studentviews.apply_internship, name="stu_apply_internship"),
    path('student/opt_out', Studentviews.opt_out, name="stu_opt_out"),
    path('student/opt_out/save', Studentviews.opt_out_save, name="stu_opt_out_save"),
    path('student/stu_logout', Studentviews.stu_logout, name="stu_logout"),

    # Company paths
    path('company/', Companyviews.company_home, name="company"),

    # Manage Company Profile
    path('company/company_profile', Companyviews.company_profile, name="company_profile"),
    path('company/company_profile/edit/<id>', Companyviews.company_profile_edit, name="company_profile_edit"),
    path('company/company_profile_editSave', Companyviews.company_profile_editSave, name="company_profile_edit_save"),

    # Manage Internship Companyside
    path('company/post_internship', Companyviews.post_internship, name="company_post_job"),
    path('company/post_internship_save', Companyviews.post_internship_save, name="company_post_job_save"),
    path('company/post_internship_edit/<post_id>', Companyviews.post_internship_edit, name="company_post_job_edit"),
    path('company/post_internship_edit_save', Companyviews.post_internship_edit_save, name="company_post_job_edit_save"),
    path('company/working_internship', Companyviews.working_internship, name="company_working_job"),
    path('company/history', Companyviews.history, name="company_history"),
    path('company/company_internship_close/<post_id>', Companyviews.company_internship_close, name="company_internship_close"),
    path('company/company_logout', Companyviews.company_logout, name="company_logout"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)