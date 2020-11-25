from django.forms import ModelForm, Textarea
from django import forms

from placement_management.models import CustomUser,Students

from placement_management.models import Companys,InternshipDetails,PlacementDrives


class StudentForm(ModelForm):
    class Meta:
        model = Students
        fields = ['enrolment_no', 'gender', 'profile_pic', 'dob', 'phone_no', 'ssc_percentage', 'hsc_percentage',
                  'ug_stream', 'ug_percentage', 'pg_cgpa']

class CompanyForm(ModelForm):
    class Meta:
        model = Companys
        fields = ['address', 'phone_no', 'website', 'company_logo']


class InternshipForm(ModelForm):
    class Meta:
        model = InternshipDetails
        fields = ['company','placementDrive','contact_person_names','designation','contact_person_numbers','contact_person_emails','company_breaf_overview','number_of_positions','internship_duration','recruitment_process','mode_of_interview','working_hours','stipend_per_month','ctc','bond_details']
        labels = {
            'placementDrive': "Select Placement Drive",
            'company_id':"Select Company",
            'number_of_positions':"No of Positions(Technology Wise)",
            'internship_duration':"Internship Duration(In Months)",
            'mode_of_interview' : "Mode of Interview(Virtual/Physical)",
            'ctc':"CTC on Confirmation (for final placement)",
            'bond_details':"Bond Details (If any)",
        }


    def __init__(self, *args, **kwargs):
        super(InternshipForm, self).__init__(*args, **kwargs)
        self.fields['company_id'].queryset = Companys.objects.all()
        self.fields['placementDrive'].queryset = PlacementDrives.objects.filter(is_completed= 0)