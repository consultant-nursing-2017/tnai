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
    tnai_number = models.CharField(max_length=200, default="TNAI number")
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS_CHOICES, default="Single")
    email = models.CharField(max_length=200, default="consultant.nursing.2017@gmail.com")
    address_line_1 = models.CharField(max_length=200, default="Address Line 1")
    address_line_2 = models.CharField(max_length=200, default="Address Line 2")
    district = models.CharField(max_length=200, choices=DISTRICT_CHOICES, default="District1")

#   Tab 2: SNC details
    degree_recognized_by_INC = models.BooleanField(default=False)
    state_nursing_council_name = models.CharField(max_length=200, choices=STATE_NURSING_COUNCIL_CHOICES, default="SNC1", blank=True)
    state_nursing_council_registration_number = models.CharField(max_length=200, default="", blank=True)
    state_nursing_council_registration_date = models.DateField(default=timezone.now, blank=True)
    state_nursing_council_proof = models.FileField(default=None, blank=True, null=True)

#   Tab 3: Educational qualifications
    # See model below
#   Tab 4: Eligibility tests
    # See model below
#   Tab 5: Passport details and misc.
    passport_number = models.CharField(max_length=50, blank=True)
    passport_valid_from = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=timezone.datetime.now().year, blank=True)
    passport_valid_to = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=timezone.datetime.now().year, blank=True)
    passport_place_of_issue = models.CharField(max_length=200, blank=True)
    preference_of_work = models.CharField(max_length=10, choices=PREFERENCE_OF_WORK_CHOICES, default="Both", blank=True)

#    def __str__(self):
#        return self.contributor + ", " + self.sponsor + ", " + self.url + ", " + self.date_submitted + ", " + self.approved

class EducationalQualifications(models.Model):
    QUALIFICATIONS_CHOICES = (
            ('10th', '10th'),
            ('12th', '12th'),
            ('Diploma', 'Diploma'),
            ('Degree', 'Degree'),
            ('Postgraduate', 'Postgraduate'),
            ('M. Phil', 'M. Phil'),
            ('PhD', 'PhD'),
    )
    YEAR_CHOICES = []
    for r in range(1970, (timezone.datetime.now().year+5)):
        YEAR_CHOICES.append((r,r))

    user = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=False)
    qualification = models.CharField(max_length=200, choices=QUALIFICATIONS_CHOICES, blank=True)
    professional_qualification_name = models.CharField(max_length=200, default="", blank=True)
    year_from = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=timezone.datetime.now().year, blank=True)
    year_to = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=timezone.datetime.now().year, blank=True)
    percentage = models.PositiveSmallIntegerField(default=0, blank=True)
    institute_name = models.CharField(max_length=200, default="", blank=True)

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

    YEAR_CHOICES = []
    for r in range(1970, (timezone.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

    user = models.ForeignKey(Candidate, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    eligibility_tests = models.CharField(max_length=20, choices=ELIGIBILITY_TESTS_CHOICES, blank=True)
    score_grade_marks = models.CharField(max_length=20, blank=True)
    completed_on = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, blank=True)
    valid_up_to = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='candidate_profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
