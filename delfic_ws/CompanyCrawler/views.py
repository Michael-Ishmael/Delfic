from django.http import JsonResponse
from django.shortcuts import render
from CompanyCrawler.models import Company

from delfic_ws.business.data import CsvLoader
from delfic_ws.business.web import WebsiteLocator


def index(request):
    return JsonResponse({"success": True, "message": "Site running..."})

def companies(request):
    companies = Company.objects.order_by('-Name')[:5]

    context = {'companies': companies_rev, 'uploadForm': form}
    return render(request, 'index.html', context)

def handle_uploaded_file(f):
    loader = CsvLoader()
    loader.handle_uploaded_file(f)


def find_company_website(request, company_ref):
    locator = WebsiteLocator()
    try:
        company_url_response = locator.find_website(company_ref)
        return JsonResponse(company_url_response)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})


def find_company_links(request):
    company_url = request.GET.get('url')
    if not company_url:
        company_url = request.POST.get('url')
    locator = WebsiteLocator()
    try:
        company_url_response = locator.find_website_links(company_url)
        json_resp = company_url_response.to_json_dict()
        return JsonResponse(json_resp)
    except Exception as ex:
        return JsonResponse({"success": False, "message": ex.message})