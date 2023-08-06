from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.management import call_command
from django.conf import settings
from firebrick.api.endpoint import Endpoint
import inspect


def get_reverse_url(instance, args=None):
    if '/' not in instance.name:
        if args:
            return reverse(instance.name, args=args)
        elif 'args'in dir(instance):
           return reverse(instance.name, args=instance.args)
        return reverse(instance.name)
    else:
        return instance.name
    
    
class ResolveUrlTest:
    '''
    Checks if a url name returns the correct view.
    '''

    def test_url_is_resolved(self):
        url = get_reverse_url(self)
        
        # Checks if the view is a class based view or function based view.
        if '__func__' in dir(self.view):
            # Checks if the `self.view` is a api `Endpoint` so it can be handled correctly
            if inspect.isclass(self.view.__self__) and issubclass(self.view.__self__, Endpoint):
                self.assertEquals(resolve(url).func, self.view)
            else:
                self.assertEquals(resolve(url).func, self.view.__func__)
        else:
            self.assertEquals(resolve(url).func.view_class, self.view)
            

class GetViewTest:
    '''
    Checks if the url returns the correct templates and status code.
    '''

    def test_GET(self):
        client = Client()
        
        url = get_reverse_url(self)
        
        response = client.get(url)

        if 'get_view_test_asserts' in dir(self):
            self.get_view_test_asserts(response)
        else:
            self.assertEquals(response.status_code, self.status)
            self.assertTemplateUsed(response, self.template)


class GETViewOr404Test:
    '''
    Checks if a view only returns a page if valid args are given.
    '''

    def test_GET_invalid_args(self):
        client = Client()

        # Load fixtures
        call_command('loaddata', *self.fixtures, verbosity=0)

        url = get_reverse_url(self, self.fail_args)

        response = client.get(url)

        if 'get_view_or_404_test_asserts_fail' in dir(self):
            self.get_view_or_404_test_asserts_fail(response)
        else:
            self.assertEquals(response.status_code, self.fail_status)
            self.assertTemplateNotUsed(response, self.success_template)

    def test_GET_valid_args(self):
        client = Client()

        # Load fixtures
        call_command('loaddata', *self.fixtures, verbosity=0)

        url = get_reverse_url(self, self.success_args)

        response = client.get(url)
        if 'get_view_or_404_test_asserts_success' in dir(self):
            self.get_view_or_404_test_asserts_success(response)
        else:
            self.assertEquals(response.status_code, self.success_status)
            self.assertTemplateUsed(response, self.success_template)


class GETLoginRequiredTest:
    '''
    Checks that a view requires user to be logged in
    '''

    def test_GET_not_logged_in(self):
        client = Client()
        
        url = get_reverse_url(self)
        
        response = client.get(url)

        self.assertRedirects(response, f'{reverse(settings.LOGIN_URL)}?next={url}')

    def test_GET_logged_in(self):
        # Creating a user
        from django.contrib.auth.models import User
        User.objects.create_user(username='testuser1', password='password1')

        client = Client()

        # Logging in to user
        client.login(username='testuser1', password='password1')
        
        url = get_reverse_url(self)
        
        response = client.get(url)

        if 'get_login_required_asserts_success' in dir(self):
            self.get_login_required_asserts_success(response)
        else:
            self.assertEquals(response.status_code, self.status)
            self.assertTemplateUsed(response, self.template)

