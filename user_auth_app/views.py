from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.views.generic.base import View

from .models import CustomUser
from .forms import CustomUserForm


class BaseView(View):

    context = {}


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
        response = render(request, self.templateName)
        return response


class RegistrationView(BaseView):

    templateName = 'user_auth_app/registration.html'

    def get(self, request):
        self.context['registration_form'] = CustomUserForm()
        response = render(request, self.templateName, self.context)
        return response

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            self.context['registration_form'] = form
        response = render(request, self.templateName, self.context)
        return response


class LogoutView(BaseView):

    def get(self, request):
        auth_logout(request)
        return redirect(reverse('login'))
