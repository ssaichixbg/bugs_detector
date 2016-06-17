from django.conf.urls import include, url, static, patterns

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bugs_detector0.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
   
    url(r'^get_count', 'www.views.get_count'),
    url(r'^detect', 'www.views.detect'),
    url(r'^$', 'www.views.home'),
    # url(r'^admin/', include(admin.site.urls)),
) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
