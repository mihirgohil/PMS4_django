from django.forms import ModelForm
from placement_management.models import CustomUser

class CreatePlacementcoordinator(ModelForm):
    class Meta:
       model = CustomUser
       fields = ['first_name']