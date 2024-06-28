from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    class_groups = models.ManyToManyField('ClassGroup', blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    nationality_1 = models.CharField(max_length=50)
    nationality_2 = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Guardian(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    occupation = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.relation})"

class ClassGroup(models.Model):
    TIER_CHOICES = [
        ('pyp', 'PYP'),
        ('myp', 'MYP'),
        ('dp', 'DP'),
    ]
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)

    def __str__(self):
        return self.name

class Student(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    class_group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True, blank=True)
    present_address = models.CharField(max_length=255)
    present_city = models.CharField(max_length=100)
    present_state = models.CharField(max_length=100)
    present_country = models.CharField(max_length=100)
    present_zip_code = models.CharField(max_length=20)
    permanent_address = models.CharField(max_length=255)
    permanent_city = models.CharField(max_length=100)
    permanent_state = models.CharField(max_length=100)
    permanent_country = models.CharField(max_length=100)
    permanent_zip_code = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='student_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AdmissionForm(models.Model):
    STATUS_CHOICES = [
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('processed', 'Processed'),
    ]
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unassigned')
    assigned_teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
    applying_for_grade = models.CharField(max_length=50)
    term = models.CharField(max_length=50)
    sibling_at_tis = models.BooleanField(default=False)

    def __str__(self):
        return f"Admission Form for {self.student}"

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('birth_certificate', 'Birth Certificate'),
        ('report_card', 'Report Card'),
        ('passport', 'Passport'),
        ('other', 'Other'),
    ]
    admission_form = models.ForeignKey(AdmissionForm, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.admission_form}"

class EmergencyContact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Emergency Contact for {self.student}"
