from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options


class SignupTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        # options.headless = True
        cls.browser = WebDriver(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_valid_signup(self):
        url = f"{self.live_server_url}{reverse('account_signup')}"
        self.browser.get(url)
        
        name_input = self.browser.find_element_by_name("name")
        name_input.send_keys('Jhon Doe')

        cpf_input = self.browser.find_element_by_name("cpf")
        cpf_input.send_keys('715.769.900-10')
        
        email_input = self.browser.find_element_by_name("email")
        email_input.send_keys('jhon@doe.com')

        password1_input = self.browser.find_element_by_name("password1")
        password1_input.send_keys('Secret#123') 

        password2_input = self.browser.find_element_by_name("password2")
        password2_input.send_keys('Secret#123')

        submit_btn = self.browser.find_element_by_xpath("//button[@type='submit']")
        submit_btn.click()
       
        # assert if after signup it was redirected to the confirm e-mail page
        confirm_url = f'{self.live_server_url}/accounts/confirm-email/'
        assert self.browser.current_url == confirm_url

    def test_invalid_signup(self):
        url = f"{self.live_server_url}{reverse('account_signup')}"
        self.browser.get(url)
        
        name_input = self.browser.find_element_by_name("name")
        name_input.send_keys('Jhon Doe')

        cpf_input = self.browser.find_element_by_name("cpf")
        cpf_input.send_keys('000.000.000-00')
        
        email_input = self.browser.find_element_by_name("email")
        email_input.send_keys('jhon@doe.com')

        password1_input = self.browser.find_element_by_name("password1")
        password1_input.send_keys('secret') 

        password2_input = self.browser.find_element_by_name("password2")
        password2_input.send_keys('secret')

        submit_btn = self.browser.find_element_by_xpath("//button[@type='submit']")
        submit_btn.click()

        # assert it was not redirected to confirm e-mail
        assert url == self.browser.current_url
        # assert it has errors showing
        assert self.browser.find_element_by_xpath("//div[@class='errors']")

