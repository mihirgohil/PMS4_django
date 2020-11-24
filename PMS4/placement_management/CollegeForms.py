from django.forms import ModelForm
from placement_management.models import CustomUser,Students

class PlacementcoordinatorForm(ModelForm):
    class Meta:
       model = CustomUser
       fields = ['first_name','last_name','email']

       def clean(self):

        # data from the form is fetched using super function
        super(PlacementcoordinatorForm, self).clean()

        # extract the username and text field from the data
        email = self.cleaned_data.get('email')

        if len(text) <10:
            self._errors['text'] = self.error_class([
                'Post Should Contain a minimum of 10 characters'])

        # return any errors if found
        return self.cleaned_data