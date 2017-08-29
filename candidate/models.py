from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Candidate(models.Model):
    GENDER_CHOICES = (
            ('Male', 'Male'),
            ('Female', 'Female'),
    )
    MARITAL_STATUS_CHOICES = (
            ('Married', 'Married'),
            ('Single', 'Single'),
    )
    DISTRICT_CHOICES = (
            ('Married', 'Married'),
            ('Single', 'Single'),
    )
    name = models.CharField(max_length=200, default="Name")
    date_of_birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default="Male")
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS_CHOICES, default="Single")
    email = models.CharField(max_length=200, default="nursing.consultant.2017@gmail.com")
    district = models.CharField(max_length=200, choices=DISTRICT_CHOICES, default="Single")
#    COUNTRY_CHOICES = (
#            ('Indian', 'Indian'),
#            ('Foreign', 'Foreign'),
#    )
#    COMPANY_CHOICES = (
#            ('Government', 'Government'),
#            ('Private', 'Private'),
#    )
#    SECTOR_CHOICES = (
#            ('Health', 'Health'),
#            ('Construction', 'Construction'),
#            ('IT', 'IT'),
#            ('Shipping', 'Shipping'),
#    )
#    name = models.CharField(max_length=200, default="Name")
#    company_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_username', default=None)
#    company_registration = models.CharField(max_length=200, default="ABC-1234")
#    company_type = models.CharField(max_length=200, choices=COMPANY_CHOICES, default="Private")
#    sector = models.CharField(max_length=200, choices=SECTOR_CHOICES, default="Health")
#    email = models.CharField(max_length=200, default="nursing.consultant.2017@gmail.com")
#    address = models.CharField(max_length=500, default="abcdef")
#    website = models.URLField(max_length=200, default="http://example.com")
#    phone = models.CharField(max_length=200, default="9810117638")
##    registration_certification = models.CharField(max_length=200, default="")
#    registration_certification = models.FileField(default="")
#    authorized_signatory_id_proof = models.FileField(default=None)
#    total_employees = models.IntegerField(default=0)
#    annual_recruitment_of_indians = models.IntegerField(default=0)
#    nurses_degree = models.IntegerField(default=0)
#    nurses_diploma = models.IntegerField(default=0)
#    doctors = models.IntegerField(default=0)
#    lab_technicians = models.IntegerField(default=0)
#    pathologists = models.IntegerField(default=0)
#    def __str__(self):
#        return self.contributor + ", " + self.sponsor + ", " + self.url + ", " + self.date_submitted + ", " + self.approved
