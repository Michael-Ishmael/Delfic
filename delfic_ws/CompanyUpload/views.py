from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from CompanyCrawler.models import Company
from CompanyUpload.forms import UploadFileForm
from delfic_ws.business.data import CsvLoader


def index(request):
    companies = Company.objects.order_by('-Name')[:5]
    companies_rev = reversed(companies)
    form = UploadFileForm()
    context = {'companies': companies_rev, 'uploadForm': form}
    return render(request, 'index.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'])
            except Exception as ex:
                return render_to_response('index.html', {'form': form, 'exception': ex.message})
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UploadFileForm()
    return render_to_response('index.html', {'form': form})


def handle_uploaded_file(f):
    loader = CsvLoader()
    loader.handle_uploaded_file(f)