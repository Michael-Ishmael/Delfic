from django.conf.urls import patterns, url
from CompanyUpload import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^uploadcompanyfile$', csrf_exempt(views.upload_file), name='fileupload'),
                       url(r'^uploadcompanyfilex$', csrf_exempt(views.upload_file_x), name='fileuploadx'),
                       url(r'^clearcompanies', csrf_exempt(views.delete_all_companies), name='clearcompanies'),
                       url(r'^addcompany', csrf_exempt(views.add_company), name='addcompany'),


)