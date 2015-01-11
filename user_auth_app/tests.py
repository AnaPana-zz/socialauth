# Create your tests here.
from django.test import LiveServerTestCase, TestCase, Client, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from selenium.webdriver.firefox.webdriver import WebDriver

from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

import unittest
import time
import os

from .views import *

PROVIDERS = {
    "google" : {'login_url' : "google-oauth2", 'site_url' : "https://accounts.google.com/"},
    "linkedin" : {'login_url' : "linkedin", 'site_url' :  "https://www.linkedin.com/"},
    "dropbox" : {'login_url' : "dropbox", 'site_url' : "https://www.dropbox.com/"},
    "facebook" : {'login_url' : "facebook", 'site_url' : "https://www.facebook.com/"},
    "github" : {'login_url' : "github", 'site_url' : "https://github.com/"},
    "vk" : {'login_url' : "vk-oauth2", 'site_url' : "http://oauth.vk.com/"},
    # "stackoverflow" : {'login_url' : "stackoverflow", 'site_url' : "https://stackexchange.com/"},
}

SKIP_UNIT_TESTS = False
SKIP_SELENIUM_TESTS = False

class ResponsesTestCase(TestCase):
    """
    Checks some HTTP responses
    302 - URL redirect
    """


    def setUp(self):
        self.c = Client()
        self.f = RequestFactory()

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_google_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['google']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_linkedin_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['linkedin']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_dropbox_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['dropbox']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_facebook_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['facebook']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_github_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['github']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skipIf(SKIP_UNIT_TESTS, 'Just skip unittests')
    def test_vk_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['vk']['login_url'])
        self.assertEqual(response.status_code, 302)

    @unittest.skip('Authorization is not working now.')
    def test_stackoverflow_response_code(self):
        response = self.c.get("/login/%s/" % PROVIDERS['stackoverflow']['login_url'])
        self.assertEqual(response.status_code, 302)



class SocialAuthGUITests(StaticLiveServerTestCase):
    """
    Class for basic literature search tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initializes web driver and virtual display for web tests.
        """
        cls.selenium = WebDriver()
        super(SocialAuthGUITests, cls).setUpClass()
        if os.environ.get('DISPLAY'): # check if X display is present
            pass
        else:  # create virtual display
            cls.display = Display(visible=0, size=(1024, 768))
            cls.display.start()


    @classmethod
    def tearDownClass(cls):
        """
        Closes driver and virtual display.
        """
        cls.selenium.quit()
        if hasattr(cls, 'display'): # for virtual display
            cls.display.stop()
        super(SocialAuthGUITests, cls).tearDownClass()


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_auth_backends(self):
        """
        """
        login_url = "{0}{1}".format(self.live_server_url, settings.LOGIN_URL)
        for provider_name, provider_params in PROVIDERS.items():
            self.selenium.get(login_url)
            link = self.selenium.find_element_by_id(provider_name)
            link.click()
            self.assertIn(provider_params['site_url'], self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_google_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("google")
        link.click()
        username, passwd = os.environ.get("GOOGLE_USERNAME"), os.environ.get('GOOGLE_PASSWD')
        email_input = self.selenium.find_element_by_id("Email")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_id("Passwd")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_id("signIn")
        submit_button.click()
        time.sleep(5) # button need time for loading
        submit_approve_access = self.selenium.find_element_by_id("submit_approve_access")
        submit_approve_access.click()
        self.assertEqual("{0}{1}".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_dropbox_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("dropbox")
        link.click()
        time.sleep(15)
        username, passwd = os.environ.get("DROPBOX_USERNAME"), os.environ.get('DROPBOX_PASSWD')
        email_input = self.selenium.find_element_by_xpath("//input[@name='login_email']")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_xpath("//input[@name='login_password']")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_xpath("//button[@type='submit']")
        submit_button.click()
        time.sleep(5) # javascript needs more time to loading
        try:
            submit_approve_access = self.selenium.find_element_by_xpath("//button[@name='allow_access']")
        except NoSuchElementException:
            pass
        else:
            submit_approve_access.click()
        self.assertEqual("{0}{1}".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_facebook_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("facebook")
        link.click()
        username, passwd = os.environ.get("FACEBOOK_USERNAME"), os.environ.get('FACEBOOK_PASSWD')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_name("pass")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_name("login")
        submit_button.click()
        # Needs to check "Submit approve access" confirmation. Now Facebook
        # skips this step.
        self.assertEqual("{0}{1}#_=_".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_linkedin_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("linkedin")
        link.click()
        username, passwd = os.environ.get("LINKEDIN_USERNAME"), os.environ.get('LINKEDIN_PASSWD')
        email_input = self.selenium.find_element_by_name("session_key")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_name("session_password")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_name("authorize")
        submit_button.click()
        self.assertEqual("{0}{1}".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_github_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("github")
        link.click()
        username, passwd = os.environ.get("GITHUB_USERNAME"), os.environ.get('GITHUB_PASSWD')
        email_input = self.selenium.find_element_by_name("login")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_name("password")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_name("commit")
        submit_button.click()
        self.assertEqual("{0}{1}".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)


    @unittest.skipIf(SKIP_SELENIUM_TESTS, "Skip selenium tests.")
    def test_vk_authorization(self):
        self.selenium.get("{0}{1}".format(self.live_server_url, settings.LOGIN_URL))
        link = self.selenium.find_element_by_id("vk")
        link.click()
        username, passwd = os.environ.get("VK_USERNAME"), os.environ.get('VK_PASSWD')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys(username)
        passwd_input = self.selenium.find_element_by_name("pass")
        passwd_input.send_keys(passwd)
        submit_button = self.selenium.find_element_by_id("install_allow")
        submit_button.click()
        self.assertEqual("{0}{1}".format(self.live_server_url, settings.LOGIN_REDIRECT_URL),
                         self.selenium.current_url)