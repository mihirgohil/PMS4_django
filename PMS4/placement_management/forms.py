from django.forms import ModelForm
from django import forms

from placement_management.models import CustomUser,Students

from placement_management.models import Companys


class StudentForm(ModelForm):
    class Meta:
        model = Students
        fields = ['enrolment_no', 'gender', 'profile_pic', 'dob', 'phone_no', 'ssc_percentage', 'hsc_percentage',
                  'ug_stream', 'ug_percentage', 'pg_cgpa']

class CompanyForm(ModelForm):
    class Meta:
        model = Companys
        fields = ['address', 'phone_no', 'website', 'company_logo']