from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.views.decorators.http import require_POST
import simplejson
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


def upload_file_x(request):
    if request.method == 'POST':
        if request.FILES is None:
            return HttpResponseRedirect('Must have files attached')

        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        file_url = '/'
        file_delete_url = '/'

        try:
            handle_uploaded_file(file)

            # generating json response array
            result = {"files": [{"name": filename,
                       "size": file_size,
                       "url": file_url,
                       "delete_url": file_delete_url,
                       "delete_type": "POST"
                      }]}
        except Exception as ex:
            result = {"files": [{"name": filename,
                       "size": file_size,
                       "error": ex.message
                      }]}

        # response_data = simplejson.dumps(result)
        return JsonResponse(result, safe=False)
    else:
        form = UploadFileForm()
        return render_to_response('index.html', {'form': form})

@require_POST
def delete_all_companies(request):
    try:
        Company.objects.all().delete()
        result = {"success": True}
    except Exception as ex:
        result = {"success": False, "message": ex.message}
    return JsonResponse(result, safe=False)

@require_POST
def add_company(request):
    try:
        data = simplejson.loads(request.body)
        if data:
            company = Company()
            company.Name = data['name']
            company.RegisteredNumber = data['registerednumber']
            company.save()
            result = {"success": True}
        else:
            result = {"success": False, "message": 'No company uploaded'}
    except Exception as ex:
        result = {"success": False, "message": ex.message}
    return JsonResponse(result)


def handle_uploaded_file(f):
    loader = CsvLoader()
    loader.handle_uploaded_file(f)