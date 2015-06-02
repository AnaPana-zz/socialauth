from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.generic.base import View
from django.utils import timezone

from .models import CustomUser
from .forms import RegistrationForm

import os


class BaseView(View):

    context = {'app_name' : 'ITSup'}


class LoggedInView(BaseView):
    templateName = 'user_auth_app/logged-in.html'

    def get(self, request):
        response = render(request, self.templateName, self.context)
        return response


class LoginView(BaseView):
    templateName = 'user_auth_app/login.html'

    def get(self, request):
        login_form = 'bla'
        # self.context['login_form'] = login_form
        response = render(request, self.templateName, self.context)
        return response


class LoginAddView(BaseView):
    """
    View for adding other social accounts
    to already authenticated user.
    """
    templateName = 'user_auth_app/login-add.html'

    def get(self, request):
        login_form = 'bla'
        # self.context['login_form'] = login_form
        response = render(request, self.templateName, self.context)
        return response


class LoginErrorView(BaseView):
    templateName = 'user_auth_app/login-error.html'

    def get(self, request):
        response = render(request, self.templateName)
        return response

class RegistrationView(BaseView):

    templateName = 'user_auth_app/registration.html'

    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect('LoginAddView')
        self.context['registration_form'] = RegistrationForm()
        response = render(request, self.templateName, self.context)
        return response

    def _send_email_with_activation_key(self, request, user_object):
        email_subject = 'Account confirmation'
        email_body = ("Hey {username}, thanks for signing up. To activate your account, click this link within"
                      "48 hours {confirm_url}").\
                        format(
                            username=user_object.username,
                            confirm_url=request.build_absolute_uri(
                                reverse('confirm', kwargs={'activation_key': user_object.activation_key}))
                        )

        send_mail(email_subject, email_body, os.environ['EMAIL_ADDRESS'],
                  (user_object.email,), fail_silently=False)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            self._send_email_with_activation_key(request, new_user)

            return redirect(reverse('home'))
        else:
            self.context['registration_form'] = form
        response = render(request, self.templateName, self.context)
        return response


class ConfirmationView(BaseView):

    templateName = 'user_auth_app/confirm.html'

    def get(self, request, activation_key):
        user = get_object_or_404(CustomUser, activation_key=activation_key)
        if user.key_expires < timezone.now():
            return render(request, 'user_auth_app/confirm_expired.html')
        user.is_active = True
        user.save()
        auth_user = authenticate(username=user.username, password=user.password)
        if auth_user is not None:
            login(request, auth_user)
            response = render(request, self.templateName, self.context)
        else:
            response = render(request, 'user_auth_app/login_failed.html', self.context)

        return response

class LogoutView(BaseView):

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))
