from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^registration/confirm/(?P<activation_key>\w+)$', ConfirmationView.as_view(), name='confirm'),
    url(r'^logged-in/$', LoggedInView.as_view(), name='logged-in'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login-error/$', LoginErrorView.as_view(), name='login-error'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
)
