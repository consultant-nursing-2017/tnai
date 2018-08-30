from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from candidate.models import EligibilityTests
from tnai.validators import ValidateFileExtension
from hashid_field import HashidAutoField, HashidField
from django.conf import settings

import datetime
import uuid
import pdb

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
    name = models.CharField(max_length=200, default="Employer Name")
    registration = models.CharField(max_length=200, default="ABC-1234")
    type = models.CharField(max_length=200, choices=COMPANY_CHOICES, default="Private")
    authorized_signatory = models.CharField(max_length=200, default="Auth 123")
    sector = models.CharField(max_length=200, choices=SECTOR_CHOICES, default="Health")
    address = models.CharField(max_length=500, default="abcdef")
    website = models.URLField(max_length=200, default="http://example.com")
    phone = models.CharField(max_length=200, default="9810117638")
#    registration_certification = models.CharField(max_length=200, default="")
    registration_certification = models.FileField(max_length = 500, default="", validators=[ValidateFileExtension.validate_file], blank=True, null=True)
    authorized_signatory_id_proof = models.FileField(max_length = 500, default=None, validators=[ValidateFileExtension.validate_file], blank=True, null=True)
    total_employees = models.IntegerField(default=0, blank=True, null=True)
    annual_recruitment_of_indians = models.IntegerField(default=0, blank=True, null=True)
    nurses_degree = models.IntegerField(default=0, blank=True, null=True)
    nurses_diploma = models.IntegerField(default=0, blank=True, null=True)
    doctors = models.IntegerField(default=0, blank=True, null=True)
    lab_technicians = models.IntegerField(default=0, blank=True, null=True)
    pathologists = models.IntegerField(default=0, blank=True, null=True)

    registration_number = HashidField(salt=settings.HASHID_FIELD_SALT+"Employer", allow_int_lookup=True, null=True, editable=False, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", default=None)
    is_provisional_registration_number = models.BooleanField(default=True, editable=False)
    sent_email_notification_provisional_registration_number = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.name + " (Employer)"

    def registration_number_display(self):
        if self.is_provisional_registration_number:
            displayed_registration_number = "TNAI/REC/PROV/" + str(self.registration_number)
        else:
            displayed_registration_number = "TNAI/REC/PERM/" + str(self.registration_number)

        return displayed_registration_number

    def save(self, *args, **kwargs):
#        pdb.set_trace()
        super(Employer, self).save(*args, **kwargs)
        if not self.registration_number:
            self.registration_number = self.pk
        super(Employer, self).save(*args, **kwargs)

    def is_employer_verified(self):
        return not self.is_provisional_registration_number

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
    GENDER_CHOICES = (
            ("Any", "Any"),
            ("Male", "Male"),
            ("Female", "Female")
    )
    employer_advert = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employer_advert', blank=True, null=True)
    dummy_employer_name = models.CharField(max_length=200, blank=True, default="")
    job_role = models.CharField(max_length=200, blank=True, default="Nurse")
    closing_date = models.DateField(blank=True, default=timezone.now)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default="Any", blank=True)
    number_of_vacancies = models.IntegerField(blank=True, default=5)
    educational_qualifications = models.CharField(max_length=500, blank=True, default="ANM required")
    eligibility_tests = models.CharField(max_length=500, blank=True, default="HAAD")
    experience = models.CharField(max_length=500, blank=True, default="2 years")
    name_of_hospital = models.CharField(max_length=200, blank=True, default="Hospital1")
    city = models.CharField(max_length=200, blank=True, default="Delhi")
    country = models.CharField(max_length=200, blank=True, default="India")
    start_date = models.DateField(blank=True, default=timezone.now)
    duration_of_assignment = models.IntegerField(blank=True, default=5)
    duration_of_assignment_units = models.CharField(max_length=15, blank=True, choices=DURATION_UNITS_CHOICES, default="Months")
    salary_number = models.IntegerField(blank=True, default=1200)
    salary_currency = models.CharField(max_length=20, blank=True, default="AED")
    allowances = models.CharField(max_length=500, blank=True, default="Travel")
    personal_accomodation = models.BooleanField(blank=True, default=False)
    family_accomodation = models.BooleanField(blank=True, default=False)
    accomodation_allowance = models.IntegerField(blank=True, default=0)
    accomodation_allowance_currency = models.CharField(max_length=20, blank=True, default="AED")
    maternity_leave_number_of_days = models.IntegerField(blank=True, default=0)
    medical_facilities = models.CharField(max_length=15, blank=True, choices=MEDICAL_FACILITIES_CHOICES, default="Self")
    visa_cost = models.BooleanField(blank=True, default=False)
    air_ticket_for_joining = models.BooleanField(blank=True, default=False)
    air_ticket_for_vacation = models.BooleanField(blank=True, default=False)
    annual_leave_days = models.IntegerField(blank=True, default=14)
    other_notes = models.CharField(max_length=500, blank=True, )
    life_insurance = models.IntegerField(blank=True, default=0)
    life_insurance_currency = models.CharField(max_length=20, blank=True, default="AED")
    obfuscated_id = HashidField(salt=settings.HASHID_FIELD_SALT+"Advertisement", allow_int_lookup=True, editable=False, alphabet="0123456789ABCDEF", null=True)

    def save(self, *args, **kwargs):
        super(Advertisement, self).save(*args, **kwargs)
        if not self.obfuscated_id:
            self.obfuscated_id = self.pk
        super(Advertisement, self).save(*args, **kwargs)

    def __str__(self):
        return "Advertisement ID: " + str(self.obfuscated_id)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='employer_profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
