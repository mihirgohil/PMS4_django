from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# Custom user class
class CustomUser(AbstractUser):
    user_type_data = ((1, "PmsCo"), (2, "Company"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

# placment Coordinator
# class Admin(models.Model):
