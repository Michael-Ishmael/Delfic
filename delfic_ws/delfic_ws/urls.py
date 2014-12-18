from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'delfic_ws.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^', include('CompanyCrawler.urls')),
                       url(r'^upload/', include('CompanyUpload.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
