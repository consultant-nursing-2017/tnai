from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import EligibilityTests

import datetime
import uuid

class Employer(models.Model):
    COUNTRY_CHOICES = (
            ('Indian', 'Indian'),
            ('Foreign', 'Foreign'),
    )
    COMPANY_CHOICES = (
            ('Government', 'Government'),
            ('Private', 'Private'),
    )
    SECTOR_CHOICES = (
            ('Health', 'Health'),
            ('Construction', 'Construction'),
            ('IT', 'IT'),
            ('Shipping', 'Shipping'),
    )
    employer_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_username', default=None, blank=True, null=True)
    country = models.CharField(max_length=200, choices = COUNTRY_CHOICES, default="Indian")
    employer_name = models.CharField(max_length=200, choices = COUNTRY_CHOICES, default="Employer Name")
    employer_registration = models.CharField(max_length=200, default="ABC-1234")
    employer_type = models.CharField(max_length=200, choices=COMPANY_CHOICES, default="Private")
    authorized_signatory = models.CharField(max_length=200, default="Auth 123")
    sector = models.CharField(max_length=200, choices=SECTOR_CHOICES, default="Health")
    address = models.CharField(max_length=500, default="abcdef")
    website = models.URLField(max_length=200, default="http://example.com")
    phone = models.CharField(max_length=200, default="9810117638")
#    registration_certification = models.CharField(max_length=200, default="")
    registration_certification = models.FileField(default="")
    authorized_signatory_id_proof = models.FileField(default=None)
    total_employees = models.IntegerField(default=0)
    annual_recruitment_of_indians = models.IntegerField(default=0)
    nurses_degree = models.IntegerField(default=0)
    nurses_diploma = models.IntegerField(default=0)
    doctors = models.IntegerField(default=0)
    lab_technicians = models.IntegerField(default=0)
    pathologists = models.IntegerField(default=0)

    def __str__(self):
        return self.employer_username.username

class Advertisement(models.Model):
    DURATION_UNITS_CHOICES = (
            ("Days", "Days"),
            ("Weeks", "Weeks"),
            ("Months", "Months"),
            ("Years", "Years"),
    )
    MEDICAL_FACILITIES_CHOICES = (
            ("Self", "Self"),
            ("Family", "Family"),
            ("None", "None"),
    )
    employer_advert = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employer_advert', blank=False, null=True)
    job_role = models.CharField(max_length=200, blank=False, default="Nurse")
    closing_date = models.DateField(blank=False, default=timezone.now)
    number_of_vacancies = models.IntegerField(blank=False, default=5)
    educational_qualifications = models.CharField(max_length=500, blank=False, default="ANM required")
    eligibility_tests = models.CharField(max_length=500, blank=False, choices=EligibilityTests.eligibility_tests_choices(), default="HAAD")
    experience = models.CharField(max_length=500, blank=False, default="2 years")
    name_of_hospital = models.CharField(max_length=200, blank=False, default="Hospital1")
    city = models.CharField(max_length=200, blank=False, default="Delhi")
    country = models.CharField(max_length=200, blank=False, default="India")
    start_date = models.DateField(blank=False, default=timezone.now)
    duration_of_assignment = models.IntegerField(blank=False, default=5)
    duration_of_assignment_units = models.CharField(max_length=15, blank=False, choices=DURATION_UNITS_CHOICES, default="Months")
    salary_number = models.IntegerField(blank=False, default=1200)
    salary_currency = models.CharField(max_length=20, blank=False, default="AED")
    allowances = models.CharField(max_length=500, blank=True, default="Travel")
    personal_accomodation = models.BooleanField(blank=True, default=False)
    family_accomodation = models.BooleanField(blank=True, default=False)
    accomodation_allowance = models.IntegerField(blank=False, default=0)
    accomodation_allowance_currency = models.CharField(max_length=20, blank=False, default="AED")
    maternity_leave = models.BooleanField(blank=True, default=False)
    medical_facilities = models.CharField(max_length=15, blank=True, choices=MEDICAL_FACILITIES_CHOICES, default="Self")
    visa_cost = models.BooleanField(blank=True, default=False)
    air_ticket_for_joining = models.BooleanField(blank=True, default=False)
    air_ticket_for_vacation = models.BooleanField(blank=True, default=False)
    annual_leave_days = models.IntegerField(blank=True, default=14)
    other_notes = models.CharField(max_length=500, blank=True, )
    life_insurance = models.IntegerField(blank=False, default=0)
    life_insurance_currency = models.CharField(max_length=20, blank=False, default="AED")
    ad_uuid = models.CharField(max_length=12, unique=True, editable=False)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='employer_profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
