from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Custom user class

from PMS4 import settings


class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminPms"), (2, "Companys"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    # email_active_field = models.BooleanField(default=True)


# placment Coordinator
class AdminPms(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField()
    objects = models.Manager()


# company side
class Companys(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone_no = models.TextField(unique=True)
    website = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    company_logo = models.ImageField()
    objects = models.Manager()

    def __str__(self):
        return self.user_type.first_name


# placement drive
class PlacementDrives(models.Model):
    id = models.AutoField(primary_key=True)
    drive_name = models.CharField(max_length=255)
    # is_active = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.drive_name


# student side
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    enrolment_no = models.TextField(unique=True)
    gender = models.CharField(max_length=255)
    profile_pic = models.ImageField(default='/media/default_avtar/user.jpg')
    # profile_pic = models.ImageField(upload_to=settings.MEDIA_ROOT + '/student_media/' + enrolment_no.__str__() + '/profile_pic')
    dob = models.DateField()
    phone_no = models.TextField()
    ssc_percentage = models.FloatField()
    hsc_percentage = models.FloatField()
    ug_stream = models.TextField()
    ug_percentage = models.FloatField()
    pg_cgpa = models.FloatField()
    placementDrive = models.ForeignKey(PlacementDrives, on_delete=models.DO_NOTHING)
    is_placed = models.BooleanField(default=False)
    is_optout = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




# job post
class InternshipDetails(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companys, on_delete=models.DO_NOTHING)
    placementDrive = models.ForeignKey(PlacementDrives, on_delete=models.DO_NOTHING)
    contact_person_names = models.CharField(blank=True, max_length=255)
    designation = models.CharField(blank=True, max_length=255)
    contact_person_numbers = models.CharField(blank=True, max_length=255)
    contact_person_emails = models.CharField(blank=True, max_length=255)
    company_breaf_overview = models.CharField(blank=True, max_length=255)
    number_of_positions = models.CharField(blank=True, max_length=255)
    internship_duration = models.CharField(blank=True, max_length=255)
    recruitment_process = models.CharField(blank=True, max_length=255)
    mode_of_interview = models.CharField(blank=True, max_length=255)
    working_hours = models.CharField(blank=True, max_length=255)
    stipend_per_month = models.CharField(blank=True, max_length=255)
    ctc = models.CharField(blank=True, max_length=255)
    bond_details = models.CharField(blank=True, max_length=255)
    is_active_registration = models.BooleanField(default=True)
    is_posted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    objects = models.Manager()





# student Applied for internship
class StudentAppliedForInternships(models.Model):
    id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(InternshipDetails, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    applied_datetime = models.DateTimeField()
    selected_date = models.DateTimeField()
    is_selected = models.BooleanField()
    objects = models.Manager()

class StudentOptOut(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    title = models.CharField(blank=True, max_length=255)
    reason = models.TextField()

# create user profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminPms.objects.create(user_type=instance)
        if instance.user_type == 2:
            Companys.objects.create(user_type=instance, address="not given", phone_no=0, website="not given",
                                    company_logo="media/default_avtar/user.jpg")
        if instance.user_type == 3:
            Students.objects.create(user_type=instance, enrolment_no="not given", gender="not given",
                                    profile_pic="media/default_avtar/user.jpg", dob="1999-01-01", phone_no="not given",
                                    ssc_percentage=0, hsc_percentage=0, ug_stream="", ug_percentage=0, pg_cgpa=0,
                                    placementDrive_id=1)


# save user profile
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminpms.save()
    if instance.user_type == 2:
        instance.companys.save()
    if instance.user_type == 3:
        instance.students.save()
