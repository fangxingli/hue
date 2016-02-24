from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wansan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_hive', 'wansan.views.get_hive', name='get_hive'),
    url(r'^$', 'wansan.views.query', name='query'),
)
