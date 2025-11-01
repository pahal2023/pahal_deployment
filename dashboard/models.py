from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# image preprocessing
def img_preprocessing(photo):

    img = Image.open(photo)
    width, height = img.size
    if width > height:  # Landscape or square-ish
        left = (width - height) / 2
        top = 0
        right = (width + height) / 2
        bottom = height
        img = img.crop((left, top, right, bottom))
    elif height > width:  # Portrait
        left = 0
        top = (height - width) / 2
        right = width
        bottom = (height + width) / 2
        img = img.crop((left, top, right, bottom))

    output_size = (200, 200)
    img.thumbnail(output_size, Image.LANCZOS)  # Use LANCZOS for high-quality down-sampling.

    output = BytesIO()
    img.save(output, format='PNG', optimize=True)  # Optimized PNG

    return output

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

    def save(self, *args, **kwargs):
        if self.pk and Student.objects.filter(pk=self.pk).exists():  # Check if updating an existing instance
            old = Student.objects.get(pk=self.pk)  # old = old_instance
            if old.photo and old.photo != self.photo:
                old.photo.delete(save=False)  # Delete old photo from S3
            else:
                super().save(*args, **kwargs)

        output = img_preprocessing(self.photo)
        self.photo = InMemoryUploadedFile(
            output, 'ImageField', f"{self.photo.name.split('.')[0]}.png",
            'image/png', sys.getsizeof(output), None
        )

        super().save(*args, **kwargs)

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
class Slot(models.Model):
    SLOT_CHOICES = [
        (1, "Monday (10:00–11:40)"),
        (2, "Monday (11:40–12:30)"),
        (3, "Tuesday (10:00–11:40)"),
        (4, "Tuesday (11:40–12:30)"),
        (5, "Wednesday (10:00–11:40)"),
        (6, "Wednesday (11:40–12:30)"),
        (7, "Thursday (10:00–11:40)"),
        (8, "Thursday (11:40–12:30)"),
        (9, "Friday (10:00–11:40)"),
        (10, "Friday (11:40–12:30"),
    ]
    slot_id = models.PositiveSmallIntegerField(choices=SLOT_CHOICES, unique=True)

    def __str__(self):
        # readable name for admin
        return dict(self.SLOT_CHOICES).get(self.slot_id, str(self.slot_id))

    class Meta:
        ordering = ['slot_id']
    
class Volunteer(models.Model):
    Reg_no = models.CharField(primary_key=True, max_length=70)
    name = models.CharField(unique=True, null=False, max_length=70)
    designation = models.CharField(max_length=25, default='Teacher')
    email = models.EmailField(max_length=80)
    phone_no = models.CharField(max_length=12)
    photo = models.ImageField(upload_to ='volunteer/', null=True)
    interest = models.CharField(max_length=40, blank=True, default='')
    experience = models.CharField(max_length=40, blank=True, default='')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='volunteers')

    slots = models.ManyToManyField(Slot, related_name='volunteers', blank=True)

    def save(self, *args, **kwargs):
        is_update = self.pk and Volunteer.objects.filter(pk=self.pk).exists()
    
        if is_update:
            old = Volunteer.objects.get(pk=self.pk)
            if old.photo and old.photo != self.photo:
                # Old photo is being replaced, delete the old one
                old.photo.delete(save=False)
                # Preprocess the new photo
                output = img_preprocessing(self.photo)
                self.photo = InMemoryUploadedFile(
                    output, 'ImageField', f"{self.photo.name.split('.')[0]}.png",
                    'image/png', sys.getsizeof(output), None
                )
            # else: photo not changed → skip reprocessing
        else:
            # New instance → process the image once
            output = img_preprocessing(self.photo)
            self.photo = InMemoryUploadedFile(
                output, 'ImageField', f"{self.photo.name.split('.')[0]}.png",
                'image/png', sys.getsizeof(output), None
            )

        super().save(*args, **kwargs)


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
