from django.conf.urls import patterns, url
from CompanyCrawler import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^company$', views.index, name='index'),
                       url(r'^company/(\w+)$', views.company, name='company'),
                       url(r'^company/(\w+)/website$', views.find_company_website, name='findcompanywebsite'),
                       url(r'^findcompanylinks/$', views.find_company_links, name='findcompanylinks'),
                       url(r'^getwebsitemeta/$', views.get_website_meta, name='getwebsitemeta'),
                       url(r'^getcalaistags/$', views.get_calais_tags, name='getcalaistags'),
                       url(r'^getPageText/$', views.get_page_text, name='getPageText'),

)
