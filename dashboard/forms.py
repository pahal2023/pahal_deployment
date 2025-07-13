from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import Student, Volunteer, Task

# Create your forms here.

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class Admission(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['active']

class VolunteerEnrolment(forms.ModelForm):
    class Meta:
        model = Volunteer
        exclude = ['status', 'user']
class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assignedTo', 'status', 'deadline','text']
        widgets = {
            'text': CKEditor5Widget(),
        }
