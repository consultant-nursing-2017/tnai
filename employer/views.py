from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Employer
from .forms import SubmitForm
from django.core.mail import send_mail

##from django.contrib.auth.decorators import permission_required


#def index(request):
#    return HttpResponse("You're at the submit_contributions index.")

class IndexView(generic.ListView):
    template_name = 'employer/index.html'
    context_object_name = 'employer_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Employer.objects.all()

def submit_employer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubmitForm(request.POST, request.FILES)
        # check whether it's valid:

        if form.is_valid():
            country = form.cleaned_data['country']
            company_username = form.cleaned_data['company_username']
            company_registration = form.cleaned_data['company_registration']
            company_type = form.cleaned_data['company_type']
            sector = form.cleaned_data['sector']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            website = form.cleaned_data['website']
            phone = form.cleaned_data['phone']
            registration_certification = form.cleaned_data['registration_certification']
            authorized_signatory_id_proof = form.cleaned_data['authorized_signatory_id_proof']
            total_employees = form.cleaned_data['total_employees']
            annual_recruitment_of_indians = form.cleaned_data['annual_recruitment_of_indians']
            nurses_degree = form.cleaned_data['nurses_degree']
            nurses_diploma = form.cleaned_data['nurses_diploma']
            doctors = form.cleaned_data['doctors']
            lab_technicians = form.cleaned_data['lab_technicians']
            pathologists = form.cleaned_data['pathologists']

            form.save()
            return HttpResponseRedirect('/employer/employer_list/')
            # if a GET (or any other method) we'll create a blank form
    else:
        form = SubmitForm()

    return render(request, 'employer/submit_employer.html', {'form': form})

class DetailView(generic.DetailView):
    model = Employer
    template_name = 'employer/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Employer.objects.all()
