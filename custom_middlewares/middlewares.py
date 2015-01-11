from django.shortcuts import render


class CatchSocialAuthExceptionMiddleware():
    def process_exception(self, request, exception):
        exception_type = exception.__class__.__name__
        if exception_type == 'AuthTokenError' or \
              exception_type == 'AuthCanceled':
            return render(request, 'auth_app/login_error.html', {'error_message' : 'Failed to login with error: "%s".' % exception})
        elif exception_type == 'UserDetailsValidationException':
            return render(request, 'auth_app/login_error.html', {'error_message' : 'Failed to create user with error: "%s".' % exception})
        else:
            raise exception
