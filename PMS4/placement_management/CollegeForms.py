from django.forms import ModelForm
from placement_management.models import CustomUser,Students
from placement_management.utilty.utility_function import *

class PlacementcoordinatorForm(ModelForm):
    class Meta:
       model = CustomUser
       fields = ['first_name','last_name','email']

    def clean(self):
        # data from the form is fetched using super function
        super(PlacementcoordinatorForm, self).clean()

        # extract the username and text field from the data
        email = self.cleaned_data.get('email')
        if check_mail(email):
            print('in validate')
            self._errors['text'] = self.error_class([
                'With this email Account Already exists'])

        # return any errors if found
        return self.cleaned_data