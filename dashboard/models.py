from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class Student(models.Model):
    roll_no = models.AutoField(primary_key=True)
    active = models.BooleanField(default=1)
    name = models.CharField(max_length=40)
    parents_name = models.CharField(max_length=40)
    address = models.CharField(max_length=40, blank=True, default='')
    phone_no = models.CharField(max_length=12)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to ='students/', null=True)
    grade = models.CharField(max_length=10, blank=True, default='')
    prev_school = models.CharField(max_length=30, blank=True, default='')

    def delete(self, *args, **kwargs):
        if self.photo:  # Check if there is an image
            self.photo.delete(save=False)

        super().delete(*args, **kwargs)  # Delete the model instance

    def __str__(self):
        return "%s. %s" % (self.roll_no, self.name)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return "%s. %s" % (self.student.name, self.date)

class Progress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="progress_repost")
    last_update = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=70)
    math = models.CharField(max_length=60, blank=True, null=True)
    hindi = models.CharField(max_length=60, blank=True, null=True)
    english = models.CharField(max_length=60, blank=True, null=True)
    extra_curricular = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return "%s. %s" % (self.student.name, self.last_update)


# STATUS CHOICES for Volunteer approval workflow
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('suspended', 'Suspended'),
]

class Volunteer(models.Model):
    Reg_no = models.CharField(primary_key=True, max_length=70)
    name = models.CharField(unique=True, null=False, max_length=70)
    designation = models.CharField(max_length=25)
    email = models.EmailField(max_length=80)
    phone_no = models.CharField(max_length=12)
    photo = models.ImageField(upload_to ='volunteer/', null=True)
    interest = models.CharField(max_length=40, blank=True, default='')
    experience = models.CharField(max_length=40, blank=True, default='')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='volunteers')

    def save(self, *args, **kwargs):
        if self.pk and Volunteer.objects.filter(pk=self.pk).exists():  # Check if updating an existing instance
            old = Volunteer.objects.get(pk=self.pk)  # old = old_instance
            if old.photo and old.photo != self.photo:
                old.photo.delete(save=False)  # Delete old photo from S3

        super().save(*args, **kwargs)  # Save the new photo

    def delete(self, *args, **kwargs):
        if self.photo:  # Check if there is an image
            self.photo.delete(save=False)

        super().delete(*args, **kwargs)  # Delete the model instance

    def __str__(self):
        return "%s. %s" % (self.name, self.designation)


class Task(models.Model):
    taskID = models.AutoField(primary_key=True)
    assignedTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_given_to")
    status = models.CharField(max_length=6)
    text = CKEditor5Field(config_name='extends')
    date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s. %s" % (self.assignedTo, self.deadline)
