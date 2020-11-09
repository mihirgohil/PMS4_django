from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# Custom user class
class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminPms"), (2, "Company"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


# placment Coordinator
class AdminPms(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField()
    objects = models.Manager()


# company side
class Companys(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone_no = models.TextField(unique=True)
    website = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    company_logo = models.ImageField()
    objects = models.Manager()


# placement drive
class PlacementDrives(models.Model):
    id = models.AutoField(primary_key=True)
    drive_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    # is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# student side
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    enrolment_no = models.TextField(unique=True)
    gender = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='student_media/'+enrolment_no.__str__()+'/profile_pic')
    dob = models.DateField()
    phone_no = models.TextField()
    ssc_percentage = models.FloatField()
    hsc_percentage = models.FloatField()
    ug_stream = models.TextField()
    ug_percentage = models.FloatField()
    pg_cgpa = models.FloatField()
    placementDrive_id = models.ForeignKey(PlacementDrives, on_delete=models.DO_NOTHING)
    is_placed = models.BooleanField(default=False)
    is_optout = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# # technologies
class Technologies(models.Model):
    id = models.AutoField(primary_key=True)
    technologies_name = models.TextField()
    objects = models.Manager()


# job post
class InternshipDetails(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Companys, on_delete=models.DO_NOTHING)
    contact_person_names = models.TextField()
    designation = models.TextField()
    contact_person_numbers = models.TextField()
    contact_person_emails = models.TextField()
    company_breaf_overview = models.TextField()
    number_of_positions = models.IntegerField()
    internship_duration = models.TextField()
    recruitment_process = models.TextField()
    mode_of_interview = models.TextField()
    working_hours = models.TextField()
    stipend_per_month = models.TextField()
    ctc = models.TextField()
    bond_details = models.TextField()
    objects = models.Manager()


#
# # job wise technologies
class IntershipWiseTechnologies(models.Model):
    id = models.AutoField(primary_key=True)
    internship_id = models.ForeignKey(InternshipDetails, on_delete=models.DO_NOTHING)
    technology_id = models.ForeignKey(Technologies, on_delete=models.DO_NOTHING)
    objects = models.Manager()


# student Applied for internship
class StudentAppliedForInternships(models.Model):
    id = models.AutoField(primary_key=True)
    internship_id = models.ForeignKey(InternshipDetails, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    technology_selected_id = models.TextField()
    applied_datetime = models.DateTimeField()
    objects = models.Manager()


# student placed for internship
class StudentSelectedForInternship(models.Model):
    id = models.AutoField(primary_key=True)
    sap_id = models.ForeignKey(StudentAppliedForInternships, on_delete=models.DO_NOTHING)
    selected_date = models.DateTimeField()
    stipend = models.FloatField()
    objects = models.Manager()


# stream posts
class StreamPosts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    body = models.TextField()
    placementDrive_id = models.ForeignKey(PlacementDrives, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# stream attachments
class StreamAttachments(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField()
    streamPost_id = models.ForeignKey(StreamPosts, on_delete=models.DO_NOTHING)
    objects = models.Manager()


# internship posted to stream
class Internship_postDetails(models.Model):
    id = models.AutoField(primary_key=True)
    registrastion_start = models.DateTimeField()
    registrastion_end = models.DateTimeField()
    is_Active = models.BooleanField(default=True)
    internship_id = models.ForeignKey(InternshipDetails, on_delete=models.DO_NOTHING)
    stream_post_id = models.ForeignKey(StreamPosts, on_delete=models.DO_NOTHING)
    objects = models.Manager()


# create user profile
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminPms.objects.create(user_type=instance)
        if instance.user_type == 2:
            Companys.objects.create(user_type=instance)
        if instance.user_type == 3:
            Students.objects.create(user_type=instance,enrolment_no = "not given", gender = "not given", profile_pic = "", dob = "1999-01-01", phone_no = "not given", ssc_percentage = 0, hsc_percentage = 0, ug_stream = "", ug_percentage = 0, pg_cgpa = 0, placementDrive_id_id = 2147483647 )


# save user profile
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminpms.save()
    if instance.user_type == 2:
        instance.compays.save()
    if instance.user_type == 3:
        instance.students.save()
