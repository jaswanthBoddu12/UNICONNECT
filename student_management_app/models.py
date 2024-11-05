
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import EmailValidator


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_organiser = models.CharField(max_length=255)
    event_held_on = models.DateField()
    event_desc = models.TextField()
    objects = models.Manager()

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    HOD = '1'
    STUDENT = '3'
    
    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'student': STUDENT
    }

    user_type_data = ((HOD, "HOD"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Clubs(models.Model):
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=255)
    club_lead = models.CharField(max_length=255, null=True, blank=True)
    club_lead_contact = models.CharField(max_length=320, null=True, blank=True, validators=[EmailValidator(message='Enter a valid email address.')])
    club_desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Notices(models.Model):
    id = models.AutoField(primary_key=True)
    notice_name = models.CharField(max_length=255)
    notice_details = models.TextField()  # New field for notice details
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    branch = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 3:
        instance.students.save()
    


