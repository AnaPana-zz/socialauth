from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'itsup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    url(r'^user_account/', include('user_auth_app.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
