from django.conf.urls import patterns, url
from CompanyUpload import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^uploadcompanyfile', views.upload_file, name='fileupload')
)