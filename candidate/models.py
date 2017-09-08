from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.contrib.postgres.fields import ArrayField

class FormYearField(models.PositiveSmallIntegerField):
    def __init__(self, *args, **kwargs):
        super (models.PositiveSmallIntegerField,self).__init__(*args, **kwargs) # populates the post
        YEAR_CHOICES = []
        for r in range(1970, (timezone.datetime.now().year+20)):
            YEAR_CHOICES.append((r,r))
        self.choices=YEAR_CHOICES

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
            ('District1', 'District1'),
            ('District2', 'District2'),
    )
    STATE_NURSING_COUNCIL_CHOICES = (
            ('SNC1', 'SNC1'),
            ('SNC2', 'SNC2'),
            ('SNC3', 'SNC3'),
    )
    PREFERENCE_OF_WORK_CHOICES = (
            ('India', 'India'),
            ('Foreign', 'Foreign'),
            ('Both', 'Both'),
    )
    YEAR_CHOICES = []
    for r in range(1970, (timezone.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

#   Tab 1: Personal details
    candidate_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate_username', default=None, blank=True, null=True)
    name = models.CharField(max_length=200, default="Name")
    fathers_name = models.CharField(max_length=200, default="Father's Name")
    date_of_birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, default="Male")
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS_CHOICES, default="Single")
#    email = models.CharField(max_length=200, default="consultant.nursing.2017@gmail.com")
    phone_number = models.CharField(max_length=200, default="9810117638")
    house_number = models.CharField(max_length=200, default="Address Line 1")
    area_locality = models.CharField(max_length=200, default="Locality")
    street_name = models.CharField(max_length=200, default="Street Nae")
    village_PS_PO = models.CharField(max_length=200, default="PS/PO/Village")
    country = models.CharField(max_length=200, default="India")
    state = models.CharField(max_length=200, default="Delhi")
    district = models.CharField(max_length=200, default="Delhi")
    pin_code = models.CharField(max_length=200, default="110078")

#   Tab 2: SNC details
#    degree_recognized_by_INC = models.BooleanField(default=False)
#    state_nursing_council_name = models.CharField(max_length=200, choices=STATE_NURSING_COUNCIL_CHOICES, default="SNC1", blank=True)
#    state_nursing_council_registration_number = models.CharField(max_length=200, default="", blank=True)
#    state_nursing_council_registration_date = models.DateField(default=timezone.now, blank=True)
#    state_nursing_council_proof = models.FileField(default=None, blank=True, null=True)

#   Tab 3: Educational qualifications
    # See model below
#   Tab 4: Eligibility tests
    # See model below
#   Tab 5: Passport details and misc.
    passport_number = models.CharField(max_length=50, blank=True)
    passport_valid_from = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    passport_valid_to = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    passport_place_of_issue = models.CharField(max_length=200, blank=True)
#   Tab 6: Miscellaneous details
    TNAI_number = models.CharField(max_length=200, default="", blank=True)
    preference_of_work = models.CharField(max_length=10, choices=PREFERENCE_OF_WORK_CHOICES, blank=True)

    def __str__(self):
        return self.candidate_username.username

class Qualifications(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    class_degree = models.CharField(max_length=200, blank=True)
    institute_name = models.CharField(max_length=200, blank=True)
    university_board_council = models.CharField(max_length=200, blank=True)
    marks_obtained = models.PositiveSmallIntegerField(default=0, blank=True)
    total_marks = models.PositiveSmallIntegerField(default=100, blank=True)
    percentage = models.PositiveSmallIntegerField(default=0, blank=True)
#    grade = models.CharField(max_length=20, default="", blank=True)
    proof = models.FileField(default=None, blank=True, null=True)

    def __str__(self):
        return self.class_degree

    class Meta:
        abstract = True

class EducationalQualifications(Qualifications):
    year_from = FormYearField(blank=True, null=True)
    year_to = FormYearField(blank=True, null=True)

class ProfessionalQualifications(Qualifications):
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)

class AdditionalQualifications(Qualifications):
    course_topic = models.CharField(max_length=200, blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
#    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=True)
#    course_name = models.CharField(max_length=200, blank=True)
#    score_marks_grade = models.CharField(max_length=20, default="", blank=True)
#    completed_on = models.DateField(blank=True, null=True)
#    proof = models.FileField(default=None, blank=True, null=True)

class EligibilityTests(models.Model):
    ELIGIBILITY_TESTS_CHOICES = (
            ('Prometric (Specify country)', 'Prometric (Specify country)'),
            ('HAAD', 'HAAD'),
            ('DHA', 'DHA'),
            ('IELTS', 'IELTS'),
            ('CGFNS', 'CGFNS'),
            ('TOEFL', 'TOEFL'),
            ('OET', 'OET'),
            ('Other', 'Other'),
    )

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=True)
    eligibility_tests = models.CharField(max_length=20, choices=ELIGIBILITY_TESTS_CHOICES, blank=True)
    country = models.CharField(max_length=100, blank=True)
#    score_grade_marks = models.CharField(max_length=20, blank=True)
    completed_on = models.DateField(blank=True, null=True)
    valid_up_to = models.DateField(blank=True, null=True)
    eligibility_proof = models.FileField(default=None, blank=True, null=True)

class Experience(models.Model):
    COUNTRY_CHOICES = (
            ('India', 'India'),
            ('Foreign', 'Foreign'),
    )

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=True)
    institution = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, choices=COUNTRY_CHOICES, blank=True)
    specialty = models.CharField(max_length=200, blank=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
#    total_years = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, blank=True)
    proof = models.FileField(default=None, blank=True, null=True)

class StateNursingCouncil(models.Model):
    COURSE_CHOICES = ['ANM', 'GNM', 'BSc.(N)']
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=True)
    course = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=200, blank=True)
    year = FormYearField(blank=True, null=True)
    @classmethod
    def course_choices(self):
        return self.COURSE_CHOICES

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='candidate_profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
